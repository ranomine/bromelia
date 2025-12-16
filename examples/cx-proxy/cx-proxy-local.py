#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    roch.cx-proxy
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains an implementation of a Diameter Cx proxy
	by using the Bromelia class features of bromelia library.
    
    :copyright: (c) 2024-present Roch-Alexandre Nomine.
"""

import os
import sys
import uuid
import logging
import pprint
import time
import requests
import yaml
from collections import OrderedDict
from threading import Lock
from typing import Optional, Tuple
from datasources.imsi_mapping import ImsiMapping, ImsiMappingManager
from datasources.customer_profile import CustomerProfile, CustomerProfileManager
import xml.etree.ElementTree as ET
import re
import asyncio

logging.basicConfig(
#    level=logging.DEBUG,
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)

basedir = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.dirname(basedir)
bromelia_dir = os.path.dirname(examples_dir)

sys.path.insert(0, bromelia_dir)

from bromelia import Bromelia
from bromelia.base import DiameterAnswer
from bromelia.avps.ietf.rfc6733 import DestinationRealmAVP, ProxyInfoAVP, ProxyHostAVP, ProxyStateAVP
from bromelia.avps.ietf.rfc6733 import VendorIdAVP, ExperimentalResultAVP, ExperimentalResultCodeAVP
from bromelia.constants import *
from bromelia.constants.experimental_result_codes import DIAMETER_ERROR_USER_UNKNOWN
from bromelia.lib.etsi_3gpp_cx import UAA # UserAuthorizationAnswer
from bromelia.lib.etsi_3gpp_cx import UAR # UserAuthorizationRequest
from bromelia.lib.etsi_3gpp_cx import MAR # MultimediaAuthRequest
from bromelia.lib.etsi_3gpp_cx import MAA # MultimediaAuthAnswer
from bromelia.lib.etsi_3gpp_cx import SAR # ServerAssignmentRequest
from bromelia.lib.etsi_3gpp_cx import SAA # ServerAssignmentAnswer
from bromelia.lib.etsi_3gpp_cx import LIR # LocationInfoRequest
from bromelia.lib.etsi_3gpp_cx import LIA # LocationInfoAnswer
from bromelia.lib.etsi_3gpp_sh import PUR # ProfileUpdateRequest
from bromelia.lib.etsi_3gpp_sh import PUA # ProfileUpdateAnswer
from bromelia.lib.etsi_3gpp_sh import UDR # UserDataRequest
from bromelia.lib.etsi_3gpp_sh import UDA # UserDataAnswer
from bromelia.lib.etsi_3gpp_sh import UserIdentityAVP as ShUserIdentityAVP
from bromelia.lib.etsi_3gpp_sh import DataReferenceAVP as ShDataReferenceAVP
from bromelia.lib.etsi_3gpp_sh import UserDataAVP as ShUserDataAVP
from bromelia.avps.etsi_3gpp.ts_129_229 import PublicIdentityAVP

def parse_username(user_name: str) -> Tuple[str, str]:
    """
    Parse a Diameter username into IMSI and realm.

    Args:
        user_name: Username in format "IMSI@realm" or just "IMSI"

    Returns:
        Tuple of (imsi, realm)
    """
    if "@" in user_name:
        imsi, realm = user_name.split("@", 1)
        return (imsi, realm)
    else:
        return (user_name, "")

def parse_public_identity(public_identity: str) -> Tuple[str, str]:
    """
    Parse a public identity into username and domain.

    Args:
        public_identity: Public identity in format "sip:username@domain"

    Returns:
        Tuple of (username, domain)
    """
    # Remove sip: prefix if present
    identity = public_identity
    if identity.startswith("sip:"):
        identity = identity[4:]
    elif identity.startswith("tel:"):
        identity = identity[4:]

    # Split on @ to get username and domain
    if "@" in identity:
        username, domain = identity.split("@", 1)
    else:
        username = identity
        domain = ""

    # Remove leading + from username if present
    if username.startswith("+"):
        username = username[1:]

    return (username, domain)

def replace_imsi(xml_data: str, new_imsi: str = None, sponsor_mcc: str = None, sponsor_mnc: str = None, as_mcc: str = None, as_mnc: str = None, force_barring_indication_zero: bool = False, public_mcc: str = None, public_mnc: str = None) -> str:
    try:
        root = ET.fromstring(xml_data)
        updated = False

        # Regex to match domain portion of 3GPP identifiers
        domain_pattern = re.compile(r"(ims\.mnc)(\d{3})(\.mcc)(\d{3})(\.3gppnetwork\.org)")

        # Regex to match SIP or TEL identities with IMSI-style user parts
        user_pattern = re.compile(r"^(sip:|tel:)?(\+?\d+)(@.*)?$")

        # Replace <IMSI> under <Extension> (only if new_imsi is provided)
        if new_imsi:
            for extension in root.findall(".//Extension"):
                imsi = extension.find("IMSI")
                if imsi is not None:
                    old_imsi = imsi.text
                    imsi.text = new_imsi
                    logging.info(f"Replaced <IMSI>: {old_imsi} → {new_imsi}")
                    updated = True
                    break

        # Replace <PrivateID>
        private_id = root.find("PrivateID")
        if private_id is not None and private_id.text:
            old_private_id = private_id.text
            parts = old_private_id.split("@")
            if len(parts) == 2:
                # Replace IMSI if provided
                user_part = new_imsi if new_imsi else parts[0]
                # Replace MCC/MNC in domain if provided
                if sponsor_mcc and sponsor_mnc:
                    new_domain = domain_pattern.sub(
                        rf"ims.mnc{sponsor_mnc.zfill(3)}.mcc{sponsor_mcc.zfill(3)}.3gppnetwork.org",
                        parts[1]
                    )
                else:
                    new_domain = parts[1]
                private_id.text = f"{user_part}@{new_domain}"
                logging.info(f"Replaced <PrivateID>: {old_private_id} → {private_id.text}")
                updated = True

        # Duplicate <PublicIdentity> blocks for sponsor and public networks
        import copy

        # Find all PublicIdentity elements
        public_identities_to_process = []
        for parent in root.iter():
            for i, elem in enumerate(parent):
                if elem.tag == "PublicIdentity":
                    public_identities_to_process.append((parent, i, elem))

        # Process in reverse to maintain correct indices when inserting
        for parent, idx, pub_id_elem in reversed(public_identities_to_process):
            # Update Identity and DisplayName within this PublicIdentity to sponsor network
            has_3gpp_identity = False
            for elem in pub_id_elem.iter():
                if elem.tag in ["Identity", "DisplayName"] and elem.text and "3gppnetwork.org" in elem.text:
                    old_text = elem.text
                    match = user_pattern.match(old_text)
                    if match:
                        has_3gpp_identity = True
                        prefix, userpart, domain = match.groups()
                        new_user = new_imsi if (new_imsi and userpart.isdigit()) else userpart
                        domain = domain or ""

                        # Update to sponsor network
                        if sponsor_mcc and sponsor_mnc:
                            sponsor_domain = domain_pattern.sub(
                                rf"ims.mnc{sponsor_mnc.zfill(3)}.mcc{sponsor_mcc.zfill(3)}.3gppnetwork.org",
                                domain
                            )
                            elem.text = f"{prefix or ''}{new_user}{sponsor_domain}"
                            logging.info(f"Updated <{elem.tag}> (sponsor): {old_text} → {elem.text}")
                            updated = True

            # Clone the entire PublicIdentity block for public network if requested
            if has_3gpp_identity and public_mcc and public_mnc:
                public_pub_id = copy.deepcopy(pub_id_elem)

                # Update all Identity and DisplayName in the cloned block to public network
                for elem in public_pub_id.iter():
                    if elem.tag in ["Identity", "DisplayName"] and elem.text and "3gppnetwork.org" in elem.text:
                        match = user_pattern.match(elem.text)
                        if match:
                            prefix, userpart, domain = match.groups()
                            new_user = new_imsi if (new_imsi and userpart.isdigit()) else userpart
                            domain = domain or ""

                            public_domain = domain_pattern.sub(
                                rf"ims.mnc{public_mnc.zfill(3)}.mcc{public_mcc.zfill(3)}.3gppnetwork.org",
                                domain
                            )
                            elem.text = f"{prefix or ''}{new_user}{public_domain}"
                            logging.info(f"Added <{elem.tag}> (public): {elem.text}")

                # Insert the cloned PublicIdentity right after the original
                parent.insert(idx + 1, public_pub_id)
                updated = True

        # Replace in <ApplicationServer>/<ServerName>
        if as_mcc and as_mnc:
            for app_server in root.findall(".//ApplicationServer"):
                server_name = app_server.find("ServerName")
                if server_name is not None and server_name.text and "3gppnetwork.org" in server_name.text:
                    old_server_name = server_name.text
                    # Replace MCC/MNC in domain
                    new_server_name = domain_pattern.sub(
                        rf"ims.mnc{as_mnc.zfill(3)}.mcc{as_mcc.zfill(3)}.3gppnetwork.org",
                        old_server_name
                    )
                    server_name.text = new_server_name
                    logging.info(f"Updated <ServerName>: {old_server_name} → {new_server_name}")
                    updated = True

        # Force BarringIndication to 0 if requested
        if force_barring_indication_zero:
            for barring_indication in root.findall(".//BarringIndication"):
                if barring_indication.text and barring_indication.text != "0":
                    old_value = barring_indication.text
                    barring_indication.text = "0"
                    logging.info(f"Forced <BarringIndication>: {old_value} → 0")
                    updated = True

        # Replace P-Visited-Network-ID in SIPHeader elements
        if public_mcc and public_mnc:
            for sip_header in root.findall(".//SIPHeader"):
                header_elem = sip_header.find("Header")
                content_elem = sip_header.find("Content")
                if (header_elem is not None and header_elem.text == "P-Visited-Network-ID" and
                    content_elem is not None and content_elem.text and "3gppnetwork.org" in content_elem.text):
                    old_content = content_elem.text
                    # Replace MCC/MNC in P-Visited-Network-ID content
                    new_content = domain_pattern.sub(
                        rf"ims.mnc{public_mnc.zfill(3)}.mcc{public_mcc.zfill(3)}.3gppnetwork.org",
                        old_content
                    )
                    content_elem.text = new_content
                    logging.info(f"Updated P-Visited-Network-ID <Content>: {old_content} → {new_content}")
                    updated = True

        if not updated:
            logging.warning("No fields were updated.")

        # Generate XML without declaration and prepend custom declaration with standalone="yes"
        xml_content = ET.tostring(root, encoding="unicode")
        return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + xml_content
    except ET.ParseError as e:
        logging.error(f"Failed to parse XML: {e}")
        return xml_data

def add_sms_parameters_to_sh_data(xml_data: str, smsc_gt: str = "14174000086") -> str:
    """
    Add SMS parameters to Sh-Data XML.

    Args:
        xml_data: The Sh-Data XML string
        smsc_gt: The SMSC Global Title to add

    Returns:
        Modified XML string with SMS parameters added
    """
    try:
        # Parse the XML
        root = ET.fromstring(xml_data)

        # Register namespaces
        ns = {
            '': 'urn:3gpp:ns:ims:user-profile',
            'op': 'urn:your-operator:sms'
        }

        # Register the namespaces for proper serialization
        ET.register_namespace('', 'urn:3gpp:ns:ims:user-profile')
        ET.register_namespace('op', 'urn:your-operator:sms')

        # Check if smsParameters already exists
        sms_params = root.find('.//{urn:your-operator:sms}smsParameters')

        if sms_params is None:
            # Create smsParameters element with operator namespace
            sms_params = ET.Element('{urn:your-operator:sms}smsParameters')
            smsc_gt_elem = ET.SubElement(sms_params, '{urn:your-operator:sms}smscGt')
            smsc_gt_elem.text = smsc_gt

            # Add after PublicIdentifiers if it exists, otherwise append at end
            public_ids = root.find('.//{urn:3gpp:ns:ims:user-profile}PublicIdentifiers')
            if public_ids is not None:
                # Find the index of PublicIdentifiers and insert after it
                for i, child in enumerate(root):
                    if child == public_ids:
                        root.insert(i + 1, sms_params)
                        break
            else:
                # Just append at the end
                root.append(sms_params)

            logging.info(f"Added SMS parameters with SMSC GT: {smsc_gt}")
        else:
            logging.info(f"SMS parameters already exist in Sh-Data")

        # Generate XML without declaration and prepend custom declaration with standalone="yes"
        xml_content = ET.tostring(root, encoding="unicode")
        return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + xml_content
    except ET.ParseError as e:
        logging.error(f"Failed to parse Sh-Data XML: {e}")
        return xml_data

def main():
    # Load diameter configuration to get error response settings
    config_file = "./config/diameter.conf.local"
    error_origin_host = None
    error_origin_realm = None

    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            error_response_config = config.get('spec', [{}])[0].get('error_response', {})
            error_origin_host = error_response_config.get('origin_host')
            error_origin_realm = error_response_config.get('origin_realm')

            if error_origin_host and error_origin_realm:
                logging.info(f"Error response config: origin_host={error_origin_host}, origin_realm={error_origin_realm}")
            else:
                logging.warning("Error response configuration not found, using defaults")
    except Exception as e:
        logging.warning(f"Failed to load error response config: {e}, using defaults")

    # Initialize IMSI mapping manager
    imsi_manager = ImsiMappingManager()
    mapping_file = "./config/imsi_mappings.json"
    try:
        count = imsi_manager.load_from_json(mapping_file)
        logging.info(f"Loaded {count} IMSI mappings from {mapping_file}")
    except FileNotFoundError:
        logging.warning(f"IMSI mapping file not found: {mapping_file}")
    except Exception as e:
        logging.error(f"Failed to load IMSI mappings: {e}")

    # Initialize customer profile manager
    profile_manager = CustomerProfileManager()
    profile_file = "./config/customer_profiles.json"
    try:
        count = profile_manager.load_from_json(profile_file)
        logging.info(f"Loaded {count} customer profiles from {profile_file}")
    except FileNotFoundError:
        logging.warning(f"Customer profile file not found: {profile_file}")
    except Exception as e:
        logging.error(f"Failed to load customer profiles: {e}")

    # Initialize Bromelia
    app = Bromelia(config_file=config_file)
    app.load_messages_into_application_id([UAR, UAA, MAR, MAA, LIR, LIA], DIAMETER_APPLICATION_Cx_Dx)
    app.load_messages_into_application_id([PUR, PUA, UDR, UDA], DIAMETER_APPLICATION_Sh)

    UAAA = app.cx.UAA   #: Creating UAA alias
    MAAA = app.cx.MAA   #: Creating MAA alias
    @app.route(application_id=DIAMETER_APPLICATION_Cx_Dx, command_code=USER_AUTHORIZATION_MESSAGE)
    def uar(request):
        # Extract and parse username from request
        received_user_name = request.user_name_avp.data.decode("utf-8") if request.has_avp("user_name_avp") else ""
        sponsored_imsi, sponsored_realm = parse_username(received_user_name)
        logging.info(f"UAR: Extracted IMSI={sponsored_imsi}, Realm={sponsored_realm}")

        # Lookup mapping
        mapping = imsi_manager.get_mapping_by_sponsored_imsi(sponsored_imsi)
        if not mapping:
            logging.warning(f"UAR: No mapping found for sponsored IMSI {sponsored_imsi}")
            # Return UAA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return UAA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"UAR: Mapped {sponsored_imsi} -> {mapping.customerImsi} (Profile: {mapping.customerProfileName})")

        # Lookup customer profile
        customerProfile = profile_manager.get_profile_by_name(mapping.customerProfileName)
        if not customerProfile:
            logging.warning(f"UAR: No profile found for {mapping.customerProfileName}")
            # Return UAA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return UAA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"UAR: Using HSS realm: {customerProfile.hssRealm}, IMS realm: {customerProfile.imsRealm}")

        uar = UAR(user_name=mapping.customerImsi + "@" + customerProfile.imsRealm,
              destination_realm=customerProfile.hssRealm,
              public_identity="sip:" + mapping.customerImsi + "@" + customerProfile.imsRealm,
              visited_network_identifier=bytes.fromhex("696d732e6d6e633132332e6d63633733322e336770706e6574776f726b2e6f7267"))

        uaa = app.send_message(uar)
        pprint.pprint(uaa.avps)

        # Transform Server-Name if present
        server_name = None
        if uaa.has_avp("server_name_avp"):
            server_name = uaa.server_name_avp.data.decode("utf-8")
            # Replace .c1. with .rbx. in the server name
            server_name = server_name.replace(".c1.", ".rbx.")
            logging.info(f"UAA: Transformed server name to {server_name}")

        # Create a new UAA with the necessary parameters from the received message
        return UAA(
                    server_name=server_name,
                    origin_host=uaa.origin_host_avp.data.decode("utf-8") if uaa.has_avp("origin_host_avp") else None,
                    origin_realm=uaa.origin_realm_avp.data.decode("utf-8") if uaa.has_avp("origin_realm_avp") else None,
                    supported_features=uaa.supported_features_avp.data if uaa.has_avp("supported_features_avp") else None,
                    experimental_result=uaa.experimental_result_avp.data if uaa.has_avp("experimental_result_avp") else None,
                    result_code=uaa.result_code_avp.data if uaa.has_avp("result_code_avp") else None,
                    )
    
    @app.route(application_id=DIAMETER_APPLICATION_Cx_Dx, command_code=MULTIMEDIA_AUTH_MESSAGE)
    def mar(request):
        # Extract and parse username from request
        received_user_name = request.user_name_avp.data.decode("utf-8") if request.has_avp("user_name_avp") else ""
        sponsored_imsi, sponsored_realm = parse_username(received_user_name)
        logging.info(f"MAR: Extracted IMSI={sponsored_imsi}, Realm={sponsored_realm}")

        # Lookup mapping
        mapping = imsi_manager.get_mapping_by_sponsored_imsi(sponsored_imsi)
        if not mapping:
            logging.warning(f"MAR: No mapping found for sponsored IMSI {sponsored_imsi}")
            # Return MAA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return MAA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"MAR: Mapped {sponsored_imsi} -> {mapping.customerImsi} (Profile: {mapping.customerProfileName})")

        # Lookup customer profile
        customerProfile = profile_manager.get_profile_by_name(mapping.customerProfileName)
        if not customerProfile:
            logging.warning(f"MAR: No profile found for {mapping.customerProfileName}")
            # Return MAA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return MAA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"MAR: Using HSS realm: {customerProfile.hssRealm}, IMS realm: {customerProfile.imsRealm}")

        mar = MAR(user_name=mapping.customerImsi + "@" + customerProfile.imsRealm,
              destination_realm=customerProfile.hssRealm,
              public_identity="sip:" + mapping.customerImsi + "@" + customerProfile.imsRealm,
              sip_number_auth_items=request.s_i_p_number_auth_items_avp.data if request.has_avp("s_i_p_number_auth_items_avp") else None,
              sip_auth_data_item=request.s_i_p_auth_data_item_avp.data if request.has_avp("s_i_p_auth_data_item_avp") else None,
              server_name=request.server_name_avp.data.decode("utf-8") if request.has_avp("server_name_avp") else None,
              )

        maa = app.send_message(mar)
        pprint.pprint(maa.avps)
        
        # Create a new UAA with the necessary parameters from the received message
        return MAA(origin_realm=maa.origin_realm_avp.data.decode("utf-8") if maa.has_avp("origin_realm_avp") else None,
                    origin_host=maa.origin_host_avp.data.decode("utf-8") if maa.has_avp("origin_host_avp") else None,
                    server_name=maa.server_name_avp.data.decode("utf-8") if maa.has_avp("server_name_avp") else None,
                    sip_auth_data_item=maa.s_i_p_auth_data_item_avp.data if maa.has_avp("s_i_p_auth_data_item_avp") else None,
                    sip_number_auth_items=maa.s_i_p_number_auth_items_avp.data if maa.has_avp("s_i_p_number_auth_items_avp") else None,
                    public_identity="sip:" + sponsored_imsi + "@ims.mnc123.mcc732.3gppnetwork.org",
                    user_name=sponsored_imsi + "@ims.mnc123.mcc732.3gppnetwork.org",
                    supported_features=maa.supported_features_avp.data if maa.has_avp("supported_features_avp") else None,
                    experimental_result=maa.experimental_result_avp.data if maa.has_avp("experimental_result_avp") else None,
                    result_code=maa.result_code_avp.data if maa.has_avp("result_code_avp") else None,
                    )

    @app.route(application_id=DIAMETER_APPLICATION_Cx_Dx, command_code=SERVER_ASSIGNMENT_MESSAGE)
    def sar(request):
        logging.info(f"Received SAR")
        pprint.pprint(request.avps)

        mapping = None
        sponsored_imsi = None
        lookup_by_imsi = False
        original_user_name = None

        # Check if User-Name AVP is present
        if request.has_avp("user_name_avp"):
            # Case 1: User-Name is present - lookup by sponsored IMSI
            received_user_name = request.user_name_avp.data.decode("utf-8")
            original_user_name = received_user_name  # Save original user_name
            sponsored_imsi, sponsored_realm = parse_username(received_user_name)
            logging.info(f"SAR: Extracted IMSI={sponsored_imsi}, Realm={sponsored_realm}")

            mapping = imsi_manager.get_mapping_by_sponsored_imsi(sponsored_imsi)
            if not mapping:
                logging.warning(f"SAR: No mapping found for sponsored IMSI {sponsored_imsi}")
                # Return SAA with DIAMETER_ERROR_USER_UNKNOWN
                experimental_result_avp = ExperimentalResultAVP([
                    VendorIdAVP(VENDOR_ID_3GPP),
                    ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
                ])
                return SAA(
                    experimental_result=experimental_result_avp.data,
                    origin_host=error_origin_host,
                    origin_realm=error_origin_realm
                )
            logging.info(f"SAR: Mapped {sponsored_imsi} -> {mapping.customerImsi} (Profile: {mapping.customerProfileName})")
            lookup_by_imsi = True

        elif request.has_avp("public_identity_avp"):
            # Case 2: Only Public-Identity is present - lookup by customer MSISDN
            received_public_identity = request.public_identity_avp.data.decode("utf-8")
            public_msisdn, public_domain = parse_public_identity(received_public_identity)
            logging.info(f"SAR: Extracted MSISDN={public_msisdn}, Domain={public_domain}")

            mapping = imsi_manager.get_mapping_by_customer_msisdn(public_msisdn)
            if not mapping:
                logging.warning(f"SAR: No mapping found for customer MSISDN {public_msisdn}")
                # Return SAA with DIAMETER_ERROR_USER_UNKNOWN
                experimental_result_avp = ExperimentalResultAVP([
                    VendorIdAVP(VENDOR_ID_3GPP),
                    ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
                ])
                return SAA(
                    experimental_result=experimental_result_avp.data,
                    origin_host=error_origin_host,
                    origin_realm=error_origin_realm
                )
            logging.info(f"SAR: Mapped MSISDN {public_msisdn} -> {mapping.customerImsi} (Profile: {mapping.customerProfileName})")
            sponsored_imsi = mapping.sponsoredImsi
            lookup_by_imsi = False

        else:
            logging.warning(f"SAR: Neither User-Name nor Public-Identity AVP found")
            # Return SAA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return SAA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        # Lookup customer profile
        customerProfile = profile_manager.get_profile_by_name(mapping.customerProfileName)
        if not customerProfile:
            logging.warning(f"SAR: No profile found for {mapping.customerProfileName}")
            # Return SAA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return SAA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"SAR: Using HSS realm: {customerProfile.hssRealm}, IMS realm: {customerProfile.imsRealm}")

        # Construct public_identity based on lookup type
        if lookup_by_imsi:
            # Case 1: User-Name was present - use customerImsi
            public_identity = "sip:" + mapping.customerImsi + "@" + customerProfile.imsRealm
            user_name = mapping.customerImsi + "@" + customerProfile.imsRealm
        else:
            # Case 2: Only Public-Identity was present - use customerMsisdn with +
            public_identity = "sip:+" + mapping.customerMsisdn + "@" + customerProfile.imsRealm
            user_name = None

        sar = SAR(destination_realm=customerProfile.hssRealm,
                    public_identity=public_identity,
                    supported_features=request.supported_features_avp.data if request.has_avp("supported_features_avp") else None,
                    server_name=request.server_name_avp.data.decode("utf-8") if request.has_avp("server_name_avp") else None,
                    user_name=user_name,
                    server_assignment_type=request.server_assignment_type_avp.data if request.has_avp("server_assignment_type_avp") else None,
                    user_data_already_available=request.user_data_already_available_avp.data if request.has_avp("user_data_already_available_avp") else None,
        )
        pprint.pprint(sar)
        sponsor_mcc = "732"
        sponsor_mnc = "123"
        public_mcc = "310"
        public_mnc = "840"
        as_mcc = "310"
        as_mnc = "840"

        saa = app.send_message(sar)

        # Process User-Data if present
        response_user_data = None
        if saa.has_avp("user_data_avp"):
            xml_payload = saa.user_data_avp.data
            if xml_payload:
                updated_xml = replace_imsi(xml_payload, sponsored_imsi, sponsor_mcc, sponsor_mnc, as_mcc, as_mnc, force_barring_indication_zero=False, public_mcc=public_mcc, public_mnc=public_mnc)
                response_user_data = updated_xml
                logging.info("Updated XML for User-Data")
            else:
                response_user_data = xml_payload

        logging.info("SAA received from HSS:")
        pprint.pprint(saa.avps)

        # Translate User-Name if present in HSS response
        response_user_name = None
        if saa.has_avp("user_name_avp"):
            # Translate User-Name: replace customer IMSI with sponsored IMSI
            response_user_name = f"{mapping.sponsoredImsi}@ims.mnc{sponsor_mnc}.mcc{sponsor_mcc}.3gppnetwork.org"
            logging.info(f"SAA: Translated User-Name to {response_user_name}")

        return SAA(origin_realm=saa.origin_realm_avp.data.decode("utf-8") if saa.has_avp("origin_realm_avp") else None,
                    origin_host=saa.origin_host_avp.data.decode("utf-8") if saa.has_avp("origin_host_avp") else None,
                    supported_features=saa.supported_features_avp.data if saa.has_avp("supported_features_avp") else None,
                    user_name=response_user_name,
                    user_data=response_user_data,
                    experimental_result=saa.experimental_result_avp.data if saa.has_avp("experimental_result_avp") else None,
                    result_code=saa.result_code_avp.data if saa.has_avp("result_code_avp") else None,
                    )

    @app.route(application_id=DIAMETER_APPLICATION_Cx_Dx, command_code=LOCATION_INFO_MESSAGE)
    def lir(request):
        logging.info(f"Received LIR")
        pprint.pprint(request.avps)

        # Extract and parse username from request
        received_public_identity = request.public_identity_avp.data.decode("utf-8") if request.has_avp("public_identity_avp") else ""
        public_msisdn, public_domain = parse_public_identity(received_public_identity)
        logging.info(f"LIR: Extracted MSISDN={public_msisdn}, Domain={public_domain}")

        # Lookup mapping
        mapping = imsi_manager.get_mapping_by_customer_msisdn(public_msisdn)
        if not mapping:
            logging.warning(f"LIR: No mapping found for Public Identity {public_msisdn}")
            # Return LIA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return LIA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"LIR: Mapped {public_msisdn} -> {mapping.customerImsi} (Profile: {mapping.customerProfileName})")

        # Lookup customer profile
        customerProfile = profile_manager.get_profile_by_name(mapping.customerProfileName)
        if not customerProfile:
            logging.warning(f"LIR: No profile found for {mapping.customerProfileName}")
            # Return LIA with DIAMETER_ERROR_USER_UNKNOWN
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return LIA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"LIR: Using HSS realm: {customerProfile.hssRealm}, IMS realm: {customerProfile.imsRealm}")

        lir = LIR(destination_realm=customerProfile.hssRealm,
                    public_identity="sip:+" + public_msisdn + "@" + customerProfile.imsRealm)

        lia = app.send_message(lir)
        pprint.pprint(lia.avps)

        return LIA(origin_realm=lia.origin_realm_avp.data.decode("utf-8") if lia.has_avp("origin_realm_avp") else None,
                    origin_host=lia.origin_host_avp.data.decode("utf-8") if lia.has_avp("origin_host_avp") else None,
                    server_name=lia.server_name_avp.data.decode("utf-8") if lia.has_avp("server_name_avp") else None,
                    result_code=lia.result_code_avp.data if lia.has_avp("result_code_avp") else None,
                    experimental_result=lia.experimental_result_avp.data if lia.has_avp("experimental_result_avp") else None,
                    )

    @app.route(application_id=DIAMETER_APPLICATION_Sh, command_code=PROFILE_UPDATE_MESSAGE)
    def pur(request):
        logging.info(f"Received PUR (Profile-Update-Request)")
        pprint.pprint(request.avps)

        # Extract User-Identity (contains Public-Identity or MSISDN)
        if not request.has_avp("user_identity_avp"):
            logging.warning(f"PUR: No User-Identity AVP found")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return PUA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        # Parse User-Identity to extract Public-Identity
        user_identity = request.user_identity_avp
        public_identity = None

        # Check if Public-Identity is present in User-Identity
        if user_identity.has_avp("public_identity_avp"):
            public_identity = user_identity.public_identity_avp.data.decode("utf-8")
            logging.info(f"PUR: Extracted Public-Identity={public_identity}")
        elif user_identity.has_avp("msisdn_avp"):
            # MSISDN is present instead of Public-Identity
            msisdn = user_identity.msisdn_avp.decode()
            logging.info(f"PUR: Extracted MSISDN={msisdn}")
            public_identity = f"sip:+{msisdn}@unknown"  # Construct a SIP URI
        else:
            logging.warning(f"PUR: Neither Public-Identity nor MSISDN found in User-Identity")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return PUA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        # Parse Public-Identity to extract MSISDN or IMSI
        sponsored_imsi = None
        public_msisdn = None

        # Track the identity type and value for reconstruction
        identity_type = None  # 'msisdn' or 'imsi'
        identity_value = None

        # Try to extract MSISDN from sip:+MSISDN@domain format
        if public_identity.startswith("sip:+"):
            public_msisdn, public_domain = parse_public_identity(public_identity)
            logging.info(f"PUR: Extracted MSISDN={public_msisdn} from Public-Identity")
            # Lookup by MSISDN
            mapping = imsi_manager.get_mapping_by_customer_msisdn(public_msisdn)
            identity_type = 'msisdn'
            identity_value = public_msisdn
        else:
            # Try to extract IMSI from sip:IMSI@domain format
            sponsored_imsi, sponsored_realm = parse_public_identity(public_identity)
            if sponsored_imsi and sponsored_imsi.isdigit():
                logging.info(f"PUR: Extracted IMSI={sponsored_imsi} from Public-Identity")
                # Lookup by sponsored IMSI
                mapping = imsi_manager.get_mapping_by_sponsored_imsi(sponsored_imsi)
                identity_type = 'imsi'
                identity_value = sponsored_imsi
            else:
                logging.warning(f"PUR: Could not extract IMSI or MSISDN from Public-Identity: {public_identity}")
                experimental_result_avp = ExperimentalResultAVP([
                    VendorIdAVP(VENDOR_ID_3GPP),
                    ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
                ])
                return PUA(
                    experimental_result=experimental_result_avp.data,
                    origin_host=error_origin_host,
                    origin_realm=error_origin_realm
                )

        if not mapping:
            logging.warning(f"PUR: No mapping found for Public-Identity {public_identity}")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return PUA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"PUR: Mapped to customer IMSI {mapping.customerImsi} (Profile: {mapping.customerProfileName})")

        # Lookup customer profile
        customerProfile = profile_manager.get_profile_by_name(mapping.customerProfileName)
        if not customerProfile:
            logging.warning(f"PUR: No profile found for {mapping.customerProfileName}")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return PUA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"PUR: Using HSS realm: {customerProfile.hssRealm}, IMS realm: {customerProfile.imsRealm}")

        # Construct new User-Identity preserving the identity type but using IMS realm
        if identity_type == 'msisdn':
            # Keep the MSISDN but replace realm with IMS realm
            new_public_identity = f"sip:+{identity_value}@{customerProfile.imsRealm}"
        else:
            # For IMSI, use customer IMSI with IMS realm
            new_public_identity = f"sip:{mapping.customerImsi}@{customerProfile.imsRealm}"

        logging.info(f"PUR: Rewriting Public-Identity from {public_identity} to {new_public_identity}")
        new_user_identity = ShUserIdentityAVP([PublicIdentityAVP(new_public_identity)])

        # Rewrite Origin-Host and Origin-Realm using customer IMS realm
        incoming_origin_host = request.origin_host_avp.data.decode("utf-8") if request.has_avp("origin_host_avp") else None
        incoming_origin_realm = request.origin_realm_avp.data.decode("utf-8") if request.has_avp("origin_realm_avp") else None

        # Extract hostname prefix from incoming Origin-Host by removing the realm part
        if incoming_origin_host and incoming_origin_realm and incoming_origin_host.endswith(incoming_origin_realm):
            hostname_prefix = incoming_origin_host[:-len(incoming_origin_realm)].rstrip('.')
            new_origin_host = f"{hostname_prefix}.{customerProfile.imsRealm}"
        elif incoming_origin_host:
            # Fallback: use first part before first dot
            hostname_prefix = incoming_origin_host.split('.')[0]
            new_origin_host = f"{hostname_prefix}.{customerProfile.imsRealm}"
        else:
            new_origin_host = f"hss.{customerProfile.imsRealm}"

        new_origin_realm = customerProfile.imsRealm
        logging.info(f"PUR: Rewriting Origin-Host from {incoming_origin_host} to {new_origin_host}")
        logging.info(f"PUR: Rewriting Origin-Realm from {incoming_origin_realm} to {new_origin_realm}")

        # Rewrite Session-Id to use new Origin-Host as first element
        incoming_session_id = request.session_id_avp.data.decode("utf-8") if request.has_avp("session_id_avp") else None
        if incoming_session_id:
            # Session-Id format: <DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]
            # Split and replace first element with new Origin-Host
            session_parts = incoming_session_id.split(';')
            if len(session_parts) > 1:
                new_session_id = f"{new_origin_host};{';'.join(session_parts[1:])}"
            else:
                # Fallback if no semicolon found
                new_session_id = incoming_session_id
            logging.info(f"PUR: Rewriting Session-Id from {incoming_session_id} to {new_session_id}")
        else:
            new_session_id = None

        # Forward PUR to HSS with translated User-Identity and Origin
        pur = PUR(
            session_id=new_session_id,
            destination_realm=customerProfile.hssRealm,
            origin_host=new_origin_host,
            origin_realm=new_origin_realm,
            user_identity=new_user_identity.data,
            data_reference=request.data_reference_avp.data if request.has_avp("data_reference_avp") else None,
            user_data=request.user_data_avp.data if request.has_avp("user_data_avp") else None
        )

        pua = app.send_message(pur)
        pprint.pprint(pua.avps)

        # Return PUA to IMS
        return PUA(
            origin_realm=pua.origin_realm_avp.data.decode("utf-8") if pua.has_avp("origin_realm_avp") else None,
            origin_host=pua.origin_host_avp.data.decode("utf-8") if pua.has_avp("origin_host_avp") else None,
            result_code=pua.result_code_avp.data if pua.has_avp("result_code_avp") else None,
            experimental_result=pua.experimental_result_avp.data if pua.has_avp("experimental_result_avp") else None,
        )

    @app.route(application_id=DIAMETER_APPLICATION_Sh, command_code=USER_DATA_MESSAGE)
    def udr(request):
        logging.info(f"Received UDR")
        pprint.pprint(request.avps)

        # Extract User-Identity from request
        if not request.has_avp("user_identity_avp"):
            logging.warning(f"UDR: No User-Identity AVP found")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return UDA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        # Parse User-Identity to extract Public-Identity or MSISDN
        user_identity_data = request.user_identity_avp
        public_identity = None

        # Try to extract Public-Identity from User-Identity grouped AVP
        # User-Identity can contain Public-Identity or MSISDN
        try:
            # Check if user_identity contains public_identity
            if hasattr(user_identity_data, 'public_identity_avp'):
                public_identity = user_identity_data.public_identity_avp.data.decode("utf-8")
                logging.info(f"UDR: Extracted Public-Identity from User-Identity: {public_identity}")
            # Check if user_identity contains msisdn
            elif hasattr(user_identity_data, 'msisdn_avp'):
                msisdn_data = user_identity_data.msisdn_avp.data
                # MSISDN is in TBCD format, need to decode
                from bromelia.utils import decode_from_tbcd
                msisdn = decode_from_tbcd(msisdn_data)
                public_identity = f"sip:+{msisdn}@unknown"
                logging.info(f"UDR: Extracted MSISDN from User-Identity: {msisdn}")
            else:
                logging.warning(f"UDR: User-Identity does not contain Public-Identity or MSISDN")
                experimental_result_avp = ExperimentalResultAVP([
                    VendorIdAVP(VENDOR_ID_3GPP),
                    ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
                ])
                return UDA(
                    experimental_result=experimental_result_avp.data,
                    origin_host=error_origin_host,
                    origin_realm=error_origin_realm
                )
        except Exception as e:
            logging.error(f"UDR: Error parsing User-Identity: {e}")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return UDA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        # Track the identity type and value for reconstruction
        identity_type = None  # 'msisdn' or 'imsi'
        identity_value = None
        mapping = None

        # Try to extract MSISDN from sip:+MSISDN@domain format
        if public_identity.startswith("sip:+"):
            public_msisdn, public_domain = parse_public_identity(public_identity)
            logging.info(f"UDR: Extracted MSISDN={public_msisdn} from Public-Identity")
            # Lookup by MSISDN
            mapping = imsi_manager.get_mapping_by_customer_msisdn(public_msisdn)
            identity_type = 'msisdn'
            identity_value = public_msisdn
        else:
            # Try to extract IMSI from sip:IMSI@domain format
            sponsored_imsi, sponsored_realm = parse_public_identity(public_identity)
            if sponsored_imsi and sponsored_imsi.isdigit():
                logging.info(f"UDR: Extracted IMSI={sponsored_imsi} from Public-Identity")
                # Lookup by sponsored IMSI
                mapping = imsi_manager.get_mapping_by_sponsored_imsi(sponsored_imsi)
                identity_type = 'imsi'
                identity_value = sponsored_imsi
            else:
                logging.warning(f"UDR: Could not extract IMSI or MSISDN from Public-Identity: {public_identity}")
                experimental_result_avp = ExperimentalResultAVP([
                    VendorIdAVP(VENDOR_ID_3GPP),
                    ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
                ])
                return UDA(
                    experimental_result=experimental_result_avp.data,
                    origin_host=error_origin_host,
                    origin_realm=error_origin_realm
                )

        if not mapping:
            logging.warning(f"UDR: No mapping found for Public-Identity {public_identity}")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return UDA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"UDR: Mapped to customer IMSI {mapping.customerImsi} (Profile: {mapping.customerProfileName})")

        # Lookup customer profile
        customerProfile = profile_manager.get_profile_by_name(mapping.customerProfileName)
        if not customerProfile:
            logging.warning(f"UDR: No profile found for {mapping.customerProfileName}")
            experimental_result_avp = ExperimentalResultAVP([
                VendorIdAVP(VENDOR_ID_3GPP),
                ExperimentalResultCodeAVP(DIAMETER_ERROR_USER_UNKNOWN)
            ])
            return UDA(
                experimental_result=experimental_result_avp.data,
                origin_host=error_origin_host,
                origin_realm=error_origin_realm
            )

        logging.info(f"UDR: Using HSS realm: {customerProfile.hssRealm}, IMS realm: {customerProfile.imsRealm}")

        # Construct new User-Identity preserving the identity type but using IMS realm
        if identity_type == 'msisdn':
            # Keep the MSISDN but replace realm with IMS realm
            new_public_identity = f"sip:+{identity_value}@{customerProfile.imsRealm}"
        else:
            # For IMSI, use customer IMSI with IMS realm
            new_public_identity = f"sip:{mapping.customerImsi}@{customerProfile.imsRealm}"

        logging.info(f"UDR: Rewriting Public-Identity from {public_identity} to {new_public_identity}")
        new_user_identity = ShUserIdentityAVP([PublicIdentityAVP(new_public_identity)])

        # Rewrite Origin-Host and Origin-Realm using customer IMS realm
        incoming_origin_host = request.origin_host_avp.data.decode("utf-8") if request.has_avp("origin_host_avp") else None
        incoming_origin_realm = request.origin_realm_avp.data.decode("utf-8") if request.has_avp("origin_realm_avp") else None

        # Extract hostname prefix from incoming Origin-Host by removing the realm part
        if incoming_origin_host and incoming_origin_realm and incoming_origin_host.endswith(incoming_origin_realm):
            hostname_prefix = incoming_origin_host[:-len(incoming_origin_realm)].rstrip('.')
            new_origin_host = f"{hostname_prefix}.{customerProfile.imsRealm}"
        elif incoming_origin_host:
            # Fallback: use first part before first dot
            hostname_prefix = incoming_origin_host.split('.')[0]
            new_origin_host = f"{hostname_prefix}.{customerProfile.imsRealm}"
        else:
            new_origin_host = f"hss.{customerProfile.imsRealm}"

        new_origin_realm = customerProfile.imsRealm
        logging.info(f"UDR: Rewriting Origin-Host from {incoming_origin_host} to {new_origin_host}")
        logging.info(f"UDR: Rewriting Origin-Realm from {incoming_origin_realm} to {new_origin_realm}")

        # Rewrite Session-Id to use new Origin-Host as first element
        incoming_session_id = request.session_id_avp.data.decode("utf-8") if request.has_avp("session_id_avp") else None
        if incoming_session_id:
            # Session-Id format: <DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]
            # Split and replace first element with new Origin-Host
            session_parts = incoming_session_id.split(';')
            if len(session_parts) > 1:
                new_session_id = f"{new_origin_host};{';'.join(session_parts[1:])}"
            else:
                # Fallback if no semicolon found
                new_session_id = incoming_session_id
            logging.info(f"UDR: Rewriting Session-Id from {incoming_session_id} to {new_session_id}")
        else:
            new_session_id = None

        # Forward UDR to HSS with translated User-Identity and Origin
        udr = UDR(
            session_id=new_session_id,
            destination_realm=customerProfile.hssRealm,
            origin_host=new_origin_host,
            origin_realm=new_origin_realm,
            user_identity=new_user_identity.data,
            data_reference=request.data_reference_avp.data if request.has_avp("data_reference_avp") else None,
            service_indication=request.service_indication_avp.data if request.has_avp("service_indication_avp") else None
        )

        uda = app.send_message(udr)
        pprint.pprint(uda.avps)

        # Process User-Data if present - add SMS parameters
        response_user_data = None
        if uda.has_avp("user_data_avp"):
            xml_payload = uda.user_data_avp.data
            if xml_payload:
                # Decode if it's bytes
                if isinstance(xml_payload, bytes):
                    xml_string = xml_payload.decode("utf-8")
                else:
                    xml_string = xml_payload

                # Add SMS parameters to the Sh-Data
                modified_xml = add_sms_parameters_to_sh_data(xml_string, smsc_gt="14174000086")

                # Encode back to bytes if original was bytes
                if isinstance(xml_payload, bytes):
                    response_user_data = modified_xml.encode("utf-8")
                else:
                    response_user_data = modified_xml

                logging.info("UDR: Extended User-Data with SMS parameters")
            else:
                response_user_data = xml_payload

        # Return UDA to IMS
        return UDA(
            origin_realm=uda.origin_realm_avp.data.decode("utf-8") if uda.has_avp("origin_realm_avp") else None,
            origin_host=uda.origin_host_avp.data.decode("utf-8") if uda.has_avp("origin_host_avp") else None,
            result_code=uda.result_code_avp.data if uda.has_avp("result_code_avp") else None,
            experimental_result=uda.experimental_result_avp.data if uda.has_avp("experimental_result_avp") else None,
            user_data=response_user_data,
        )

    # Register the request handler
#    app.route(DIAMETER_APPLICATION_Cx, handle_request)

    # Run the application
    app.run()

if __name__ == "__main__":
    main()

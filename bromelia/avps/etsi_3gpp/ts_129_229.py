# -*- coding: utf-8 -*-
"""
    bromelia.etsi_3gpp.ts_129_229
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains Diameter AVP classes defined in ETSI TS 129 229.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import annotations
from ..ietf.rfc6733 import VendorIdAVP
from ..ietf.rfc6733 import UserNameAVP
from ..ietf.rfc4590 import DigestAlgorithmAVP
from ..ietf.rfc4590 import DigestHA1AVP
from ..ietf.rfc4590 import DigestQoPAVP
from ..ietf.rfc4590 import DigestRealmAVP


from ...base import DiameterAVP
from ...constants.etsi_3gpp.ts_129_229 import *
from ...types import *


class FeatureListIdAVP(DiameterAVP, Unsigned32Type):
    """Implementation of Feature-List-ID AVP in Section 6.3.30 of
    ETSI TS 129 229 V14.3.0 (2019-10).

    The Feature-List-ID AVP (AVP Code 629) is of type Unsigned32.
    """
    code = FEATURE_LIST_ID_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             FeatureListIdAVP.code,
                             FeatureListIdAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class FeatureListAVP(DiameterAVP, Unsigned32Type):
    """Implementation of Feature-List AVP in Section 6.3.31 of 
    ETSI TS 129 229 V14.3.0 (2019-10).

    The Feature-List AVP (AVP Code 630) is of type Unsigned32.
    """
    code = FEATURE_LIST_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data=convert_to_4_bytes(0)):
        DiameterAVP.__init__(self, 
                             FeatureListAVP.code,
                             FeatureListAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SupportedFeaturesAVP(DiameterAVP, GroupedType):
    """Implementation of Supported-Features AVP in Section 6.3.29 of 
    ETSI TS 129 229 V14.3.0 (2019-10).

    The Supported-Features AVP (AVP Code 628) is of type Grouped.
    """
    code = SUPPORTED_FEATURES_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "vendor_id": VendorIdAVP,
                    "feature_list_id": FeatureListIdAVP,
                    "feature_list": FeatureListAVP
    }
    optionals = {}

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SupportedFeaturesAVP.code,
                             SupportedFeaturesAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class VisitedNetworkIdentifierAVP(DiameterAVP, OctetStringType):
    """Implementation of Visited-Network-Identifier AVP in Section 6.3.1  
    of ETSI TS 129 229 V15.2.0 (2019-10).

    The Visited-Network-Identifier AVP (AVP Code 600) is of type OctetString.
    """
    code = VISITED_NETWORK_IDENTIFIER_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             VisitedNetworkIdentifierAVP.code,
                             VisitedNetworkIdentifierAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPNumberAuthItemsAVP(DiameterAVP, Unsigned32Type):
    """Implementation of SIP-Number-Auth-Items AVP in Section 6.3.8 
    of ETSI TS 129 229 V16.2.0 (2020-11).

    The SIP-Number-Auth-Items AVP (AVP Code 607) is of type Unsigned32.
    """
    code = SIP_NUMBER_AUTH_ITEMS_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPNumberAuthItemsAVP.code,
                             SIPNumberAuthItemsAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPAuthenticationSchemeAVP(DiameterAVP, UTF8StringType):
    """Implementation of SIP-Authentication-Scheme AVP in Section 6.3.9 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The SIP-Authentication-Scheme AVP (AVP Code 608) is of type UTF8String.
    """
    code = SIP_AUTHENTICATION_SCHEME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPAuthenticationSchemeAVP.code,
                             SIPAuthenticationSchemeAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPAuthenticateAVP(DiameterAVP, OctetStringType):
    """Implementation of SIP-Authenticate AVP in Section 6.3.10 
    of ETSI TS 129 229 V16.2.0 (2020-11).

    The SIP-Authenticate AVP (AVP Code 609) is of type OctetString.
    """
    code = SIP_AUTHENTICATE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPAuthenticateAVP.code,
                             SIPAuthenticateAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPAuthorizationAVP(DiameterAVP, OctetStringType):
    """Implementation of SIP-Authorization AVP in Section 6.3.11 
    of ETSI TS 129 229 V16.2.0 (2020-11).

    The SIP-Authorization AVP (AVP Code 610) is of type OctetString.
    """
    code = SIP_AUTHORIZATION_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPAuthorizationAVP.code,
                             SIPAuthorizationAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ConfidentialityKeyAVP(DiameterAVP, OctetStringType):
    """Implementation of Confidentiality-Key AVP in Section 6.3.27 
    of ETSI TS 129 229 V16.2.0 (2020-11).

    The Confidentiality-Key AVP (AVP Code 625) is of type OctetString.
    """
    code = CONFIDENTIALITY_KEY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ConfidentialityKeyAVP.code,
                             ConfidentialityKeyAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class IntegrityKeyAVP(DiameterAVP, OctetStringType):
    """Implementation of Integrity-Key AVP in Section 6.3.28
    of ETSI TS 129 229 V16.2.0 (2020-11).

    The Integrity-Key AVP (AVP Code 626) is of type OctetString.
    """
    code = INTEGRITY_KEY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             IntegrityKeyAVP.code,
                             IntegrityKeyAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class AssociatedRegisteredIdentitiesAVP(DiameterAVP, GroupedType):
    """Implementation of Associated-Registered-Identities AVP in Section 6.3.50 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Associated-Registered-Identities AVP (AVP Code 647) is of type Grouped.
    """
    code = ASSOCIATED_REGISTERED_IDENTITIES_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    optionals = {
                    "user_name": UserNameAVP,
    }

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             AssociatedRegisteredIdentitiesAVP.code,
                             AssociatedRegisteredIdentitiesAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPItemNumberAVP(DiameterAVP, Unsigned32Type):
    """Implementation of SIP-Item-Number AVP in Section 6.3.14 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The SIP-Item-Number AVP (AVP Code 613) is of type Unsigned32.
    """

    code = SIP_ITEM_NUMBER_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPItemNumberAVP.code,
                             SIPItemNumberAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPAuthDataItemAVP(DiameterAVP, GroupedType):
    """Implementation of SIP-Auth-Data-Item AVP in Section 6.3.50 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The SIP-Auth-Data-Item AVP (AVP Code 612) is of type Grouped.
    """
    code = SIP_AUTH_DATA_ITEM_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    optionals = {
                    "sip_item_number": SIPItemNumberAVP,
    }

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPAuthDataItemAVP.code,
                             SIPAuthDataItemAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ServerAssignmentTypeAVP(DiameterAVP, EnumeratedType):
    """Implementation of Server-Assignment-Type AVP in Section 6.3.15 
    of ETSI TS 129 229 V16.2.0 (2020-11).

    The Server-Assignment-Type AVP (AVP Code 614) is of type Enumerated.
    """
    code = SERVER_ASSIGNMENT_TYPE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                SERVER_ASSIGNMENT_TYPE_NO_ASSIGNMENT,
                SERVER_ASSIGNMENT_TYPE_REGISTRATION,
                SERVER_ASSIGNMENT_TYPE_RE_REGISTRATION,
                SERVER_ASSIGNMENT_TYPE_UNREGISTERED_USER,
                SERVER_ASSIGNMENT_TYPE_TIMEOUT_DEREGISTRATION,
                SERVER_ASSIGNMENT_TYPE_USER_DEREGISTRATION,
                SERVER_ASSIGNMENT_TYPE_DEREGISTRATION_STORE_SERVER_NAME,
                SERVER_ASSIGNMENT_TYPE_USER_DEREGISTRATION_STORE_SERVER_NAME,
                SERVER_ASSIGNMENT_TYPE_ADMINISTRATIVE_DEREGISTRATION,
                SERVER_ASSIGNMENT_TYPE_AUTHENTICATION_FAILURE,
                SERVER_ASSIGNMENT_TYPE_AUTHENTICATION_TIMEOUT,
                SERVER_ASSIGNMENT_TYPE_DEREGISTRATION_TOO_MUCH_DATA,
                SERVER_ASSIGNMENT_TYPE_AAA_USER_DATA_REQUEST,
                SERVER_ASSIGNMENT_TYPE_PGW_UPDATE,
                SERVER_ASSIGNMENT_TYPE_RESTORATION
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ServerAssignmentTypeAVP.code,
                             ServerAssignmentTypeAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ReasonCodeAVP(DiameterAVP, EnumeratedType):
    """Implementation of Reason-Code AVP in Section 6.3.17 
    of ETSI TS 129 229 V11.3.0 (2013-04).

    The Reason-Code AVP (AVP Code 616) is of type Enumerated.
    """
    code = REASON_CODE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                REASON_CODE_PERMANENT_TERMINATION,
                REASON_CODE_NEW_SERVER_ASSIGNED,
                REASON_CODE_SERVER_CHANGE,
                REASON_CODE_REMOVE_S_CSCF,
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ReasonCodeAVP.code,
                             ReasonCodeAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ReasonInfoAVP(DiameterAVP, UTF8StringType):
    """Implementation of Reason-Info AVP in Section 6.3.18
    of ETSI TS 129 229 V11.3.0 (2013-04).

    The Reason-Info AVP (AVP Code 617) is of type UTF8String.
    """
    code = REASON_INFO_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ReasonInfoAVP.code,
                             ReasonInfoAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class WildcardedPublicIdentityAVP(DiameterAVP, UTF8StringType):
    """Implementation of Wildcarded-Public-Identity AVP in Section 6.3.35
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Wildcarded-Public-Identity AVP (AVP Code 634) is of type UTF8String.
    """
    code = WILDCARDED_PUBLIC_IDENTITY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             WildcardedPublicIdentityAVP.code,
                             WildcardedPublicIdentityAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class DeregistrationReasonAVP(DiameterAVP, GroupedType):
    """Implementation of Deregistration-Reason AVP in Section 6.3.16 
    of ETSI TS 129 229 V11.3.0 (2013-04).

    The Server-Assignment-Type AVP (AVP Code 615) is of type Grouped.
    """
    code = DEREGISTRATION_REASON_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "reason_code": ReasonCodeAVP,
    }
    optionals = {
                    "reason_info": ReasonInfoAVP,
    }

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             DeregistrationReasonAVP.code,
                             DeregistrationReasonAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class PublicIdentityAVP(DiameterAVP, UTF8StringType):
    """Implementation of Public-Identity AVP in Section 6.3.2 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Public-Identity AVP (AVP Code 601) is of type UTF8String.
    """
    code = PUBLIC_IDENTITY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             PublicIdentityAVP.code,
                             PublicIdentityAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ServerNameAVP(DiameterAVP, UTF8StringType):
    """Implementation of Server-Name AVP in Section 6.3.3 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Server-Name AVP (AVP Code 602) is of type UTF8String.
    """
    code = SERVER_NAME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ServerNameAVP.code,
                             ServerNameAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class PriviledgedSenderIndicationAVP(DiameterAVP, EnumeratedType):
    """Implementation of Priviledged-Sender-Indication AVP in Section 6.3.58 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Priviledged-Sender-Indication AVP (AVP Code 652) is of type Enumerated.
    """
    code = PRIVILEDGED_SENDER_INDICATION_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                PRIVILEDGED_SENDER_INDICATION_NOT_PRIVILEDGED_SENDER,
                PRIVILEDGED_SENDER_INDICATION_PRIVILEDGED_SENDER
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             PriviledgedSenderIndicationAVP.code,
                             PriviledgedSenderIndicationAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)

class UserAuthorizationTypeAVP(DiameterAVP, EnumeratedType):
    """Implementation of User-Authorization-Type AVP in Section 6.3.24 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The User-Authorization-Type AVP (AVP Code 623) is of type Enumerated.
    """
    code = USER_AUTHORIZATION_TYPE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                USER_AUTHORIZATION_TYPE_REGISTRATION,
                USER_AUTHORIZATION_TYPE_DE_REGISTRATION,
                USER_AUTHORIZATION_TYPE_REGISTRATION_AND_CAPABILITIES
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             UserAuthorizationTypeAVP.code,
                             UserAuthorizationTypeAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class UserDataAlreadyAvailableAVP(DiameterAVP, EnumeratedType):
    """Implementation of User-Data-Already-Available AVP in Section 6.3.26 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The User-Data-Already-Available AVP (AVP Code 624) is of type Enumerated.
    """
    code = USER_DATA_ALREADY_AVAILABLE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                USER_DATA_ALREADY_AVAILABLE_USER_DATA_NOT_AVAILABLE,
                USER_DATA_ALREADY_AVAILABLE_USER_DATA_ALREADY_AVAILABLE
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             UserDataAlreadyAvailableAVP.code,
                             UserDataAlreadyAvailableAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class MultipleRegistrationIndicationAVP(DiameterAVP, EnumeratedType):
    """Implementation of Multiple-Registration-Indication AVP in Section 6.3.51 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Multiple-Registration-Indication AVP (AVP Code 648) is of type Enumerated.
    """
    code = MULTIPLE_REGISTRATION_INDICATION_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                MULTIPLE_REGISTRATION_INDICATION_NOT_MULTIPLE_REGISTRATION,
                MULTIPLE_REGISTRATION_INDICATION_MULTIPLE_REGISTRATION
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             MultipleRegistrationIndicationAVP.code,
                             MultipleRegistrationIndicationAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class UARFlagsAVP(DiameterAVP, Unsigned32Type):
    """Implementation of UAR-Flags AVP in Section 6.3.44 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The UAR-Flags AVP (AVP Code 637) is of type Unsigned32.
    """

    code = UAR_FLAGS_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             UARFlagsAVP.code,
                             UARFlagsAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SARFlagsAVP(DiameterAVP, Unsigned32Type):
    """Implementation of SAR-Flags AVP in Section 6.3.63 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The SAR-Flags AVP (AVP Code 655) is of type Unsigned32.
    """

    code = SAR_FLAGS_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SARFlagsAVP.code,
                             SARFlagsAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)
        
        
class RTRFlagsAVP(DiameterAVP, Unsigned32Type):
    """Implementation of RTR-Flags AVP in Section 6.3.69 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The RTR-Flags AVP (AVP Code 659) is of type Unsigned32.
    """

    code = RTR_FLAGS_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             RTRFlagsAVP.code,
                             RTRFlagsAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)
        
        
class LIAFlagsAVP(DiameterAVP, Unsigned32Type):
    """Implementation of LIA-Flags AVP in Section 6.3.69 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The LIA-Flags AVP (AVP Code 653) is of type Unsigned32.
    """

    code = LIA_FLAGS_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             LIAFlagsAVP.code,
                             LIAFlagsAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)
        
        
class MandatoryCapabilityAVP(DiameterAVP, Unsigned32Type):
    """Implementation of Mandatory-Capability AVP in Section 6.3.5 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Mandatory-Capability AVP (AVP Code 604) is of type Unsigned32.
    """

    code = MANDATORY_CAPABILITY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             MandatoryCapabilityAVP.code,
                             MandatoryCapabilityAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class OptionalCapabilityAVP(DiameterAVP, Unsigned32Type):
    """Implementation of Optional-Capability AVP in Section 6.3.6 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Optional-Capability AVP (AVP Code 605) is of type Unsigned32.
    """

    code = OPTIONAL_CAPABILITY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             OptionalCapabilityAVP.code,
                             OptionalCapabilityAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class InitialCSeqSequenceNumberAVP(DiameterAVP, Unsigned32Type):
    """Implementation of Initial-CSeq-Sequence-Number AVP in Section 6.3.62 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Initial-CSeq-Sequence-Number AVP (AVP Code 654) is of type Unsigned32.
    """

    code = INITIAL_CSEQ_SEQUENCE_NUMBER_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             InitialCSeqSequenceNumberAVP.code,
                             InitialCSeqSequenceNumberAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class RegistrationTimeOutAVP(DiameterAVP, TimeType):
    """Implementation of Registration-Time-Out AVP in Section 6.3.71 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Registration-Time-Out AVP (AVP Code 661) is of type Time.
    """

    code = REGISTRATION_TIME_OUT_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             RegistrationTimeOutAVP.code,
                             RegistrationTimeOutAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        Unsigned32Type.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)

class ServerCapabilitiesAVP(DiameterAVP, GroupedType):
    """Implementation of Server-Capabilities AVP in Section 6.3.4 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Supported-Features AVP (AVP Code 603) is of type Grouped.
    """
    code = SERVER_CAPABILITIES_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {}

    optionals = {
                    "mandatory_capability": MandatoryCapabilityAVP,
                    "optional_capability": OptionalCapabilityAVP,
                    "server_name": ServerNameAVP
    }

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ServerCapabilitiesAVP.code,
                             ServerCapabilitiesAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class IdentityWithEmergencyRegistrationAVP(DiameterAVP, GroupedType):
    """Implementation of Identity-with-Emergency-Registration AVP in Section 6.3.57 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Identity-with-Emergency-Registration AVP (AVP Code 651) is of type Grouped.
    """
    code = IDENTITY_WITH_EMERGENCY_REGISTRATION_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "user_name": UserNameAVP,
                    "public_identity": PublicIdentityAVP,
    }

    optionals = {}

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             IdentityWithEmergencyRegistrationAVP.code,
                             IdentityWithEmergencyRegistrationAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class WebRTCAuthenticationFunctionNameAVP(DiameterAVP, UTF8StringType):
    """Implementation of WebRTC-Authentication-Function-Name AVP in Section 6.3.65 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The WebRTC-Authentication-Function-Name AVP (AVP Code 657) is of type UTF8String.
    """
    code = WEBRTC_AUTHENTICATION_FUNCTION_NAME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             WebRTCAuthenticationFunctionNameAVP.code,
                             WebRTCAuthenticationFunctionNameAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPAuthenticationSchemeAVP(DiameterAVP, UTF8StringType):
    """Implementation of SIP-Authentication-Scheme AVP in Section 6.3.9 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The SIP-Authentication-Scheme AVP (AVP Code 608) is of type UTF8String.
    """
    code = SIP_AUTHENTICATION_SCHEME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPAuthenticationSchemeAVP.code,
                             SIPAuthenticationSchemeAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class WebRTCWebServerFunctionNameAVP(DiameterAVP, UTF8StringType):
    """Implementation of WebRTC-Web-Server-Function-Name AVP in Section 6.3.66 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The WebRTC-Web-Server-Function-Name AVP (AVP Code 658) is of type UTF8String.
    """
    code = WEBRTC_WEB_SERVER_FUNCTION_NAME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             WebRTCWebServerFunctionNameAVP.code,
                             WebRTCWebServerFunctionNameAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        UTF8StringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class AllowedWAFWWSFIdentitiesAVP(DiameterAVP, GroupedType):
    """Implementation of Allowed-WAF-WWSF-Identities AVP in Section 6.3.64 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Allowed-WAF-WWSF-Identities (AVP Code 656) is of type Grouped.
    """
    code = ALLOWED_WAF_WWSF_IDENTITIES_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {}

    optionals = {
                    "webrtc_authentication_function_name": WebRTCAuthenticationFunctionNameAVP,
                    "webrtc_web_server_function_name": WebRTCWebServerFunctionNameAVP,
    }

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             AllowedWAFWWSFIdentitiesAVP.code,
                             AllowedWAFWWSFIdentitiesAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SIPDigestAuthenticateAVP(DiameterAVP, GroupedType):
    """Implementation of SIP-Digest-Authenticate AVP in Section 6.3.36 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The SIP-Digest-Authenticate (AVP Code 637) is of type Grouped.
    """
    code = SIP_DIGEST_AUTHENTICATE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "digest_realm": DigestRealmAVP,
                    "digest_qop": DigestQoPAVP,
                    "digest_ha1": DigestHA1AVP,
    }

    optionals = {
                    "digest_algorithm": DigestAlgorithmAVP,
    }

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SIPDigestAuthenticateAVP.code,
                             SIPDigestAuthenticateAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class UserDataAVP(DiameterAVP, OctetStringType):
    """Implementation of User-Data AVP in Section 6.3.7  
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The User-Data AVP (AVP Code 606) is of type OctetString.
    """
    code = USER_DATA_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             UserDataAVP.code,
                             UserDataAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class PathAVP(DiameterAVP, OctetStringType):
    """Implementation of Path AVP in Section 6.3.47  
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Path AVP (AVP Code 640) is of type OctetString.
    """
    code = PATH_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             PathAVP.code,
                             PathAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ContactAVP(DiameterAVP, OctetStringType):
    """Implementation of Contact AVP in Section 6.3.48  
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Contact AVP (AVP Code 641) is of type OctetString.
    """
    code = CONTACT_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ContactAVP.code,
                             ContactAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class CallIDSIPHeaderAVP(DiameterAVP, OctetStringType):
    """Implementation of Call-ID-SIP-Header AVP in Section 6.3.49.1  
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Call-ID-SIP-Header AVP (AVP Code 643) is of type OctetString.
    """
    code = CALL_ID_SIP_HEADER_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             CallIDSIPHeaderAVP.code,
                             CallIDSIPHeaderAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class FromSIPHeaderAVP(DiameterAVP, OctetStringType):
    """Implementation of From-SIP-Header AVP in Section 6.3.49.2  
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The From-SIP-Header AVP (AVP Code 644) is of type OctetString.
    """
    code = FROM_SIP_HEADER_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             FromSIPHeaderAVP.code,
                             FromSIPHeaderAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ToSIPHeaderAVP(DiameterAVP, OctetStringType):
    """Implementation of To-SIP-Header AVP in Section 6.3.49.3  
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The To-SIP-Header AVP (AVP Code 645) is of type OctetString.
    """
    code = TO_SIP_HEADER_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ToSIPHeaderAVP.code,
                             ToSIPHeaderAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class RecordRouteAVP(DiameterAVP, OctetStringType):
    """Implementation of Record-Route AVP in Section 6.3.49.4  
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Record-Route AVP (AVP Code 646) is of type OctetString.
    """
    code = RECORD_ROUTE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             RecordRouteAVP.code,
                             RecordRouteAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class OriginatingRequestAVP(DiameterAVP, EnumeratedType):
    """Implementation of Originating-Request AVP in Section 6.3.34 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Originating-Request AVP (AVP Code 633) is of type Enumerated.
    """
    code = ORIGINATING_REQUEST_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                ORIGINATING_REQUEST_ORIGINATING
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             OriginatingRequestAVP.code,
                             OriginatingRequestAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SessionPriorityAVP(DiameterAVP, EnumeratedType):
    """Implementation of Session-Priority AVP in Section 6.3.34 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Session-Priority AVP (AVP Code 650) is of type Enumerated.
    """
    code = SESSION_PRIORITY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                SESSION_PRIORITY_PRIORITY_0,
                SESSION_PRIORITY_PRIORITY_1,
                SESSION_PRIORITY_PRIORITY_2,
                SESSION_PRIORITY_PRIORITY_3,
                SESSION_PRIORITY_PRIORITY_4,
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SessionPriorityAVP.code,
                             SessionPriorityAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)

class PrimaryEventChargingFunctionNameAVP(DiameterAVP, DiameterIdentityType):
    """Implementation of Primary-Event-Charging-Function-Name AVP in Section 6.3.20 of
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Primary-Event-Charging-Function-Name AVP (AVP Code 619) is of type DiameterIdentity.
    """
    code = PRIMARY_EVENT_CHARGING_FUNCTION_NAME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             PrimaryEventChargingFunctionNameAVP.code,
                             PrimaryEventChargingFunctionNameAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        DiameterIdentityType.__init__(self, data=data)


class SecondaryEventChargingFunctionNameAVP(DiameterAVP, DiameterIdentityType):
    """Implementation of Secondary-Event-Charging-Function-Name AVP in Section 6.3.21 of
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Secondary-Event-Charging-Function-Name AVP (AVP Code 620) is of type DiameterIdentity.
    """
    code = SECONDARY_EVENT_CHARGING_FUNCTION_NAME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             SecondaryEventChargingFunctionNameAVP.code,
                             SecondaryEventChargingFunctionNameAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        DiameterIdentityType.__init__(self, data=data)        

class PrimaryChargingCollectionFunctionNameAVP(DiameterAVP, DiameterIdentityType):
    """Implementation of Primary-Charging-Collection-Function-Name AVP in Section 6.3.22 of
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Primary-Charging-Collection-Function-Name AVP (AVP Code 621) is of type DiameterIdentity.
    """
    code = PRIMARY_CHARGING_COLLECTION_FUNCTION_NAME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             PrimaryChargingCollectionFunctionNameAVP.code,
                             PrimaryChargingCollectionFunctionNameAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        DiameterIdentityType.__init__(self, data=data)        


class SecondaryChargingCollectionFunctionNameAVP(DiameterAVP, DiameterIdentityType):
    """Implementation of Secondary-Charging-Collection-Function-Name AVP in Section 6.3.23 of
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Secondary-Charging-Collection-Function-Name AVP (AVP Code 622) is of type DiameterIdentity.
    """
    code = SECONDARY_CHARGING_COLLECTION_FUNCTION_NAME_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             SecondaryChargingCollectionFunctionNameAVP.code,
                             SecondaryChargingCollectionFunctionNameAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        DiameterIdentityType.__init__(self, data=data)        


class ChargingInformationAVP(DiameterAVP, GroupedType):
    """Implementation of Charging-Information AVP in Section 6.3.19 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Charging-Information AVP (AVP Code 618) is of type Grouped.
    """
    code = CHARGING_INFORMATION_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {}

    optionals = {
                    "primary_event_charging_function_name": PrimaryEventChargingFunctionNameAVP,
                    "secondary_event_charging_function_name": SecondaryEventChargingFunctionNameAVP,
                    "primary_charging_collection_function_name": PrimaryChargingCollectionFunctionNameAVP,
                    "secondary_charging_collection_function_name": SecondaryChargingCollectionFunctionNameAVP,
    }

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             ChargingInformationAVP.code,
                             ChargingInformationAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class AssociatedIdentitiesAVP(DiameterAVP, GroupedType):
    """Implementation of Associated-Identities AVP in Section 6.3.33 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Associated-Identities AVP (AVP Code 632) is of type Grouped.
    """
    code = ASSOCIATED_IDENTITIES_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {}

    optionals = {
                    "user_name": UserNameAVP
    }
     

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             AssociatedIdentitiesAVP.code,
                             AssociatedIdentitiesAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class LooseRouteInformationAVP(DiameterAVP, EnumeratedType):
    """Implementation of Loose-Route-Indication AVP in Section 6.3.45 
    of ETSI TS 129 229 V16.3.0 (2024-10).

    The Loose-Route-Indication AVP (AVP Code 638) is of type Enumerated.
    """
    code = LOOSE_ROUTE_INDICATION_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
                LOOSE_ROUTE_INDICATION_LOOSE_ROUTE_NOT_REQUIRED,
                LOOSE_ROUTE_INDICATION_LOOSE_ROUTE_REQUIRED
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             LooseRouteInformationAVP.code,
                             LooseRouteInformationAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SubscriptionInfoAVP(DiameterAVP, GroupedType):
    """Implementation of Subscription-Info AVP in Section 6.3.49 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Subscription-Info AVP (AVP Code 642) is of type Grouped.
    """
    code = SUBSCRIPTION_INFO_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "call_id_sip_header": CallIDSIPHeaderAVP,
                    "from_sip_header": FromSIPHeaderAVP,
                    "to_sip_header": ToSIPHeaderAVP,
                    "record_route": RecordRouteAVP,
                    "contact": ContactAVP,
    }

    optionals = {}

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SubscriptionInfoAVP.code,
                             SubscriptionInfoAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class PCSCFSubscriptionInfoAVP(DiameterAVP, GroupedType):
    """Implementation of P-CSCF-Subscription-Info AVP in Section 6.3.70 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The P-CSCF-Subscription-Info AVP (AVP Code 660) is of type Grouped.
    """
    code = P_CSCF_SUBSCRIPTION_INFO_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "call_id_sip_header": CallIDSIPHeaderAVP,
                    "from_sip_header": FromSIPHeaderAVP,
                    "to_sip_header": ToSIPHeaderAVP,
                    "contact": ContactAVP,
    }

    optionals = {}
     

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             PCSCFSubscriptionInfoAVP.code,
                             PCSCFSubscriptionInfoAVP.vendor_id)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class RestorationInfoAVP(DiameterAVP, GroupedType):
    """Implementation of Restoration-Info AVP in Section 6.3.52 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Restoration-Info AVP (AVP Code 649) is of type Grouped.
    """
    code = RESTORATION_INFO_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "path": PathAVP,
                    "contact": ContactAVP
    }

    optionals = {
                    "initial_cseq_sequence_number": InitialCSeqSequenceNumberAVP,
                    "call_id_sip_header": CallIDSIPHeaderAVP,
                    "subscription_info": SubscriptionInfoAVP,
                    "p_cscf_subscription_info": PCSCFSubscriptionInfoAVP,
    }
     

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             RestorationInfoAVP.code,
                             RestorationInfoAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class SCSCFRestorationInfoAVP(DiameterAVP, GroupedType):
    """Implementation of SCSCF-Restoration-Info AVP in Section 6.3.46 of 
    ETSI TS 129 229 V16.3.0 (2024-10).

    The SCSCF-Restoration-Info AVP (AVP Code 639) is of type Grouped.
    """
    code = SCSCF_RESTORATION_INFO_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {
                    "user_name": UserNameAVP,
                    "restoration_info": RestorationInfoAVP
    }

    optionals = {
                    "registration_time_out": RegistrationTimeOutAVP,
                    "sip_authentication_scheme": SIPAuthenticationSchemeAVP
    }
     

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             SCSCFRestorationInfoAVP.code,
                             SCSCFRestorationInfoAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)

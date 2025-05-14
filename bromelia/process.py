# -*- coding: utf-8 -*-
"""
    bromelia.process
    ~~~~~~~~~~~~~~~~

    This module contains all implementations for handling the Diameter 
    messages processing step. It contains classes for creating and 
    parsing Diameter Requests and Answers.

    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""
import logging
import re

from .avps import AuthRequestTypeAVP
from .constants import *
from .exceptions import ProcessRequestException
from .utils import is_answer_message
from .utils import is_request_message

process_message_logging = logging.getLogger("ProcessDiameterMessage")


def process_request(association, message):
    list_of_avps_by_code = [avp.code for avp in message.avps]

    connection = association.connection

    local_node_host_name = connection.local_node.host_name.encode("utf-8")
    local_node_realm = connection.local_node.realm.encode("utf-8")
    proxied_realms_patterns = connection.proxy_realms

    if DESTINATION_HOST_AVP_CODE in list_of_avps_by_code:
        if not list(filter(lambda avp: avp.data == local_node_host_name, message.avps)):
            logging.debug(f"[{message.header.hop_by_hop.hex()}] Diameter "\
                          f"Request has Destination-Host AVP, however it was "\
                          f"addressed to another node.")
            
            raise ProcessRequestException("Request does not comply with "\
                                          "local consumption rules.")

        logging.debug(f"[{message.header.hop_by_hop.hex()}] Diameter Request "\
                      f"has Destination-Host AVP and contains the hostname of "\
                      f"local node.")

    elif (DESTINATION_HOST_AVP_CODE not in list_of_avps_by_code and 
          DESTINATION_REALM_AVP_CODE in list_of_avps_by_code):

        destination_realm_avp = next((avp for avp in message.avps if avp.code == DESTINATION_REALM_AVP_CODE), None)
        if not destination_realm_avp:
            logging.error(f"[{message.header.hop_by_hop.hex()}] Destination-Realm AVP code found but AVP itself is missing.")
            raise ProcessRequestException("Internal error: Destination-Realm AVP missing.")

        destination_realm = destination_realm_avp.data.decode("utf-8")
        realm_is_valid_for_proxy = False

        if proxied_realms_patterns and isinstance(proxied_realms_patterns, list):
            for pattern_str in proxied_realms_patterns:
                try:
                    if re.match(pattern_str, destination_realm):
                        realm_is_valid_for_proxy = True
                        logging.debug(f"[{message.header.hop_by_hop.hex()}] Destination-Realm '{destination_realm}' matched PROXY_REALMS pattern '{pattern_str}'.")
                        break 
                except re.error as e:
                    logging.error(f"[{message.header.hop_by_hop.hex()}] Invalid regex pattern '{pattern_str}' in PROXY_REALMS: {e}")
            
            if not realm_is_valid_for_proxy:
                logging.debug(f"[{message.header.hop_by_hop.hex()}] Diameter Request's Destination-Realm '{destination_realm}' "
                              f"did not match any PROXY_REALMS patterns.")
                raise ProcessRequestException("Request's Destination-Realm does not match any configured PROXY_REALMS patterns.")

        if not realm_is_valid_for_proxy:
            if destination_realm.encode("utf-8") != local_node_realm:
                logging.debug(f"[{message.header.hop_by_hop.hex()}] Diameter "
                              f"Request does not include Destination-Host AVP, "
                              f"and its Destination-Realm AVP ('{destination_realm}') was not in PROXY_REALMS "
                              f"and does not match local realm ('{local_node_realm.decode('utf-8')}').")
                raise ProcessRequestException("Request does not comply with "
                                              "local consumption or proxy rules.")
            else:
                 logging.debug(f"[{message.header.hop_by_hop.hex()}] Diameter Request "
                               f"is for local consumption (Destination-Realm matches local realm).")

        logging.debug(f"[{message.header.hop_by_hop.hex()}] Diameter Request "\
                      f"does not include Destination-Host AVP, but it does "\
                      f"include a valid Destination-Realm AVP.")
        
    elif (DESTINATION_HOST_AVP_CODE not in list_of_avps_by_code and 
          DESTINATION_REALM_AVP_CODE not in list_of_avps_by_code):

        logging.debug(f"[{message.header.hop_by_hop.hex()}] Diameter Request "\
                      f"does not include neither Destination-Host AVP nor "\
                      f"Destination-Realm AVP.")

    else:
        raise ProcessRequestException("Request does not comply with local "\
                                      "consumption rules.")

    association.num_requests += 1
    logging.debug(f"[{message.header.hop_by_hop.hex()}] Processed Diameter Request.")


def process_answer(association, message):
    end_to_end_key = message.header.end_to_end.hex()
    hop_by_hop_key = message.header.hop_by_hop.hex()

    if end_to_end_key in association.end_to_end_identifiers:
        if hop_by_hop_key in association.pending_requests:
            if message.header.end_to_end == association.pending_requests[hop_by_hop_key].header.end_to_end:
                association.pending_requests.pop(hop_by_hop_key)
                association.num_answers += 1
    
    logging.debug(f"[{message.header.hop_by_hop.hex()}] Processed Diameter Answer.")


class ProcessDiameterMessage:
    @staticmethod
    def process_answer_from_existing_pending_request(association, message):
        process_message_logging.debug("Processing Diameter Answer.")

        end_to_end_key = message.header.end_to_end.hex()
        hop_by_hop_key = message.header.hop_by_hop.hex()

        if end_to_end_key in association.end_to_end_identifiers:
            if hop_by_hop_key in association.pending_requests:
                if message.header.end_to_end == association.pending_requests[hop_by_hop_key].header.end_to_end:
                    association.pending_requests.pop(hop_by_hop_key)

    
    @staticmethod
    def is_valid_origin_host_avp(avp, connection):
        if avp.code == ORIGIN_HOST_AVP_CODE:
            
            process_message_logging.debug(f"Origin-Host AVP validation.")

            checklist_mandatory_info = 0
        
            process_message_logging.debug(f"flags: {avp.get_flags()}.")
            if avp.flags == FLAG_NOT_VENDOR_SPECIFIC_AND_MANDATORY_AND_NOT_PROTECTED:
                checklist_mandatory_info += 1
            
            process_message_logging.debug(f"length: {avp.get_length()}.")
            if avp.get_length() == AVP_HEADER_LENGTH + len(avp.data):
                checklist_mandatory_info += 1

            data = avp.data.decode("utf-8")
            process_message_logging.debug(f"data: {data}.")
            if data == connection.peer_node.host_name:
                checklist_mandatory_info += 1


            if checklist_mandatory_info == 3:
                process_message_logging.debug(f"Result: PASS.")
                return True
            process_message_logging.debug(f"Result: FAIL.")
            return False


    @staticmethod
    def is_valid_origin_realm_avp(avp, connection):
        if avp.code == ORIGIN_REALM_AVP_CODE:
            process_message_logging.debug(f"Origin-Realm AVP validation.")

            checklist_mandatory_info = 0
        
            process_message_logging.debug(f"flags: {avp.get_flags()}.")
            if avp.flags == FLAG_NOT_VENDOR_SPECIFIC_AND_MANDATORY_AND_NOT_PROTECTED:
                checklist_mandatory_info += 1
            
            process_message_logging.debug(f"length: {avp.get_length()}.")
            if avp.get_length() == AVP_HEADER_LENGTH + len(avp.data):
                checklist_mandatory_info += 1

            data = avp.data.decode("utf-8")
            process_message_logging.debug(f"data: {data}.")
            if data == connection.peer_node.realm:
                checklist_mandatory_info += 1


            if checklist_mandatory_info == 3:
                process_message_logging.debug(f"Result: PASS.")
                return True
            process_message_logging.debug(f"Result: FAIL.")
            return False


    @staticmethod
    def is_valid_origin_state_id_avp(avp, connection):
        if (avp.code == ORIGIN_STATE_ID_AVP_CODE):
            return True
        return False


    @staticmethod
    def is_valid_result_code_avp(avp):
        if avp.code == RESULT_CODE_AVP_CODE:
            
            process_message_logging.debug(f"Result-Code AVP validation.")

            checklist_mandatory_info = 0
        
            process_message_logging.debug(f"flags: {avp.get_flags()}.")
            if avp.flags == FLAG_NOT_VENDOR_SPECIFIC_AND_MANDATORY_AND_NOT_PROTECTED:
                checklist_mandatory_info += 1
            
            process_message_logging.debug(f"length: {avp.get_length()}.")
            if avp.get_length() == AVP_LENGTH_UNSIGNED32:
                checklist_mandatory_info += 1

            process_message_logging.debug(f"data: {avp.data.hex()}.")


            if checklist_mandatory_info == 2:
                process_message_logging.debug(f"Result: PASS.")
                return True
            process_message_logging.debug(f"Result: FAIL.")
            return False


    @staticmethod
    def is_valid_disconnect_cause_avp(avp):
        if (avp.code == DISCONNECT_CAUSE_AVP_CODE) and (avp.data == DISCONNECT_CAUSE_REBOOTING):
            return True
        return False


    @staticmethod
    def is_valid_host_ip_address_avp(avp, connection):
        if (avp.code == HOST_IP_ADDRESS_AVP_CODE):
            host_ip_address = "{}.{}.{}.{}".format(int(avp.data[2]),int(avp.data[3]),int(avp.data[4]),int(avp.data[5]))
            return True
            # if connection.peer_node.ip_address == host_ip_address:
            #     return True
            # process_message_logging.debug("Host IP Address from Peer Node not valid!")
            # return False


    @staticmethod
    def is_valid_product_name_avp(avp, connection):
        if (avp.code == PRODUCT_NAME_AVP_CODE):
            return True
        return False


    @staticmethod
    def is_valid_vendor_id_avp(avp, connection):
        if (avp.code == VENDOR_ID_AVP_CODE):
            return True
        return False


    @staticmethod
    def is_valid_session_id_avp(avp):
        if avp.code == SESSION_ID_AVP_CODE:
            process_message_logging.debug(f"Session-Id AVP validation.")

            checklist_mandatory_info = 0
        
            process_message_logging.debug(f"flags: {avp.get_flags()}.")
            if avp.flags == FLAG_NOT_VENDOR_SPECIFIC_AND_MANDATORY_AND_NOT_PROTECTED:
                checklist_mandatory_info += 1
            
            process_message_logging.debug(f"length: {avp.get_length()}.")
            if avp.get_length() == (AVP_HEADER_LENGTH + len(avp.data)):
                checklist_mandatory_info += 1

            process_message_logging.debug(f"data: {avp.data.hex()}.")


            if checklist_mandatory_info == 2:
                process_message_logging.debug(f"Result: PASS.")
                return True
            process_message_logging.debug(f"Result: FAIL.")
            return False


    @staticmethod
    def is_valid_auth_application_id_avp(avp):
        if avp.code == AUTH_APPLICATION_ID_AVP_CODE:
            process_message_logging.debug(f"Auth-Application-Id AVP validation.")

            checklist_mandatory_info = 0
        
            process_message_logging.debug(f"flags: {avp.get_flags()}.")
            if avp.flags == FLAG_NOT_VENDOR_SPECIFIC_AND_MANDATORY_AND_NOT_PROTECTED:
                checklist_mandatory_info += 1

            process_message_logging.debug(f"length: {avp.get_length()}.")
            if avp.get_length() == AVP_LENGTH_UNSIGNED32:
                checklist_mandatory_info += 1
        

            if checklist_mandatory_info == 2: # == 3
                process_message_logging.debug(f"Result: PASS.")
                return True
            process_message_logging.debug(f"Result: FAIL.")
            return False


    @staticmethod
    def is_valid_auth_request_type_avp(avp):
        if avp.code == AUTH_REQUEST_TYPE_AVP_CODE:
            process_message_logging.debug(f"Auth-Request-Type AVP validation.")

            checklist_mandatory_info = 0
        
            process_message_logging.debug(f"flags: {avp.get_flags()}.")
            if avp.flags == FLAG_NOT_VENDOR_SPECIFIC_AND_MANDATORY_AND_NOT_PROTECTED:
                checklist_mandatory_info += 1
            
            process_message_logging.debug(f"length: {avp.get_length()}.")
            if avp.get_length() == AVP_LENGTH_INTEGER32:
                checklist_mandatory_info += 1

            process_message_logging.debug(f"data: {avp.data.hex()}.")
            if avp.data in AuthRequestTypeAVP.values:
                checklist_mandatory_info += 1


            if checklist_mandatory_info == 3:
                process_message_logging.debug(f"Result: PASS.")
                return True
            process_message_logging.debug(f"Result: FAIL.")
            return False


class ProcessCapabilityExchange():
    def __init__(self, association, message):
        self.association = association
        self.connection = association.connection
        self.message = message

        self.checklist_mandatory_avps = 0
        self.checklist_optional_avps = 0
        self.checklist_error_avps = 0
        self.is_valid = False

        if message.header.flags == FLAG_REQUEST:
            self.process_request()
        elif message.header.flags == FLAG_RESPONSE:
            self.process_answer()
        else:
            """What should we do if find an error?"""
            pass


    def process_request(self):
        for avp in self.message.avps:
            if ProcessDiameterMessage.is_valid_origin_host_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_realm_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_host_ip_address_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_vendor_id_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_product_name_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_state_id_avp(avp, self.connection):
                self.checklist_optional_avps += 1


        if (self.checklist_mandatory_avps == 5) and (self.checklist_optional_avps >= 0 and self.checklist_optional_avps <= 7):
            self.is_valid = True
        else:
            self.is_valid = False


    def process_answer(self):
        ProcessDiameterMessage.process_answer_from_existing_pending_request(self.association, self.message)
        for avp in self.message.avps:
            if ProcessDiameterMessage.is_valid_result_code_avp(avp):
                self.checklist_mandatory_avps += 1

            if ProcessDiameterMessage.is_valid_origin_host_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_realm_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_host_ip_address_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_vendor_id_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_product_name_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_state_id_avp(avp, self.connection):
                self.checklist_optional_avps += 1


        if (self.checklist_mandatory_avps == 6) and (self.checklist_optional_avps >= 0 or self.checklist_optional_avps <= 7):
            self.is_valid = True
        else:
            self.is_valid = False


class ProcessDeviceWatchdog():
    def __init__(self, association, message):
        self.association = association
        self.connection = association.connection
        self.message = message

        self.checklist_mandatory_avps = 0
        self.checklist_optional_avps = 0
        self.checklist_error_avps = 0
        self.is_valid = False

        if message.header.flags == FLAG_REQUEST:
            self.process_request()
        elif message.header.flags == FLAG_RESPONSE:
            self.process_answer()
        else:
            """What should we do if find an error?"""
            pass


    def process_request(self):
        for avp in self.message.avps:
            if ProcessDiameterMessage.is_valid_origin_host_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_realm_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_state_id_avp(avp, self.connection):
                self.checklist_optional_avps += 1


        if (self.checklist_mandatory_avps == 2) and (self.checklist_optional_avps == 0 or self.checklist_optional_avps == 1):
            self.is_valid = True
        else:
            self.is_valid = False


    def process_answer(self):
        ProcessDiameterMessage.process_answer_from_existing_pending_request(self.association, self.message)

        for avp in self.message.avps:
            if ProcessDiameterMessage.is_valid_result_code_avp(avp):
                self.checklist_mandatory_avps += 1

            if ProcessDiameterMessage.is_valid_origin_host_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_realm_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_state_id_avp(avp, self.connection):
                self.checklist_optional_avps += 1


        if (self.checklist_mandatory_avps == 3) and (self.checklist_optional_avps == 0 or self.checklist_optional_avps == 1):
            self.is_valid = True
        else:
            self.is_valid = False


class ProcessDisconnectPeer():
    def __init__(self, association, message):
        self.association = association
        self.connection = association.connection
        self.message = message

        self.checklist_mandatory_avps = 0
        self.checklist_optional_avps = 0
        self.checklist_error_avps = 0
        self.is_valid = False

        if message.header.flags == FLAG_REQUEST:
            self.process_request()
        elif message.header.flags == FLAG_RESPONSE:
            self.process_answer()
        else:
            """What should we do if find an error?"""
            pass


    def process_request(self):
        for avp in self.message.avps:
            if ProcessDiameterMessage.is_valid_origin_host_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_realm_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_disconnect_cause_avp(avp):
                self.checklist_mandatory_avps += 1


        if (self.checklist_mandatory_avps == 3):
            self.is_valid = True
        else:
            self.is_valid = False


    def process_answer(self):
        ProcessDiameterMessage.process_answer_from_existing_pending_request(self.association, self.message)

        for avp in self.message.avps:
            if ProcessDiameterMessage.is_valid_result_code_avp(avp):
                self.checklist_mandatory_avps += 1

            if ProcessDiameterMessage.is_valid_origin_host_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1

            elif ProcessDiameterMessage.is_valid_origin_realm_avp(avp, self.connection):
                self.checklist_mandatory_avps += 1


        if (self.checklist_mandatory_avps == 3) and (self.checklist_error_avps >= 0 and self.checklist_error_avps <= 2):
            self.is_valid = True
        else:
            self.is_valid = False


class BaseMessageProcessor:
    def __init__(self, association):
        self.association = association


    def is_valid_capability_exchange(self, msg):
        process = ProcessCapabilityExchange(self.association, msg)
        return process.is_valid


    def is_valid_device_watchdog(self, msg):
        process = ProcessDeviceWatchdog(self.association, msg)
        return process.is_valid


    def is_valid_disconnect_peer(self, msg):
        process = ProcessDisconnectPeer(self.association, msg)
        return process.is_valid


    def create_answer(self, msg):
        if msg.header.command_code == CAPABILITIES_EXCHANGE_MESSAGE:
            answer = self.association.base.cea
    
        elif msg.header.command_code == DEVICE_WATCHDOG_MESSAGE:
            answer = self.association.base.dwa

        elif msg.header.command_code == DISCONNECT_PEER_MESSAGE:
            answer = self.association.base.dpa

        answer.header.hop_by_hop = msg.header.hop_by_hop
        answer.header.end_to_end = msg.header.end_to_end

        return answer


    def check_message(self, msg):
        if is_answer_message(msg):
            process_answer(self.association, msg)
            
        elif is_request_message(msg):
            process_request(self.association, msg)

# -*- coding: utf-8 -*-
"""
    bromelia.lib.etsi_3gpp_cx.messages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the Diameter protocol messages for 3GPP Cx/Dx 
    Application Id.

    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

import platform
import socket

from .avps import *

from ...base import DiameterRequest, DiameterAnswer
from ...constants import *


class UserAuthorizationAnswer(DiameterAnswer):
    """Implementation of User-Authorization-Answer (UAA) command as per 
    clause 6.1.2 of ETSI TS 129 229 V16.3.0 (2024-10).

    The User-Authorization-Answer is indicated by the Command Code field
    set to 300 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import UAA
        >>> uaa = UAA()
        >>> uaa
        <Diameter Message: 300 [UAA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    # "drmp": DRMPAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    # "oc_supported_features": OCSupportedFeaturesAVP,
                    # "oc_olr": OCOLRAVP,
                    # "load": LoadAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "server_name": ServerNameAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 oc_supported_features=None,
                 oc_olr=None,
                 load=None,
                 supported_features=None,
                 server_name=None,
                 server_capabilities=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=USER_AUTHORIZATION_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterAnswer._load(self, locals())


class UserAuthorizationRequest(DiameterRequest):
    """Implementation of User-Authorization-Request (UAR) command as per 
    clause 6.1.1 of ETSI TS 129 229 V16.3.0 (2024-10).

    The User-Authorization-Request is indicated by the Command Code 
    field set to 300 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import UAR
        >>> uar_avps = {
        ...     "destination_realm": "example.com",
        ...     "user_name": "frodo",
        ...     "public_identity": "ims.example.com",
        ...     "visited_network_identifier": bytes.fromhex("696d732e6d6e633132332e6d63633733322e336770706e6574776f726b2e6f7267")
        ... }
        >>> uar = UAR(**uar_avps)
        >>> uar
        <Diameter Message: 300 [UAR] REQ|PXY, 16777216 [3GPP Cx], 8 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_name": UserNameAVP,
                    "public_identity": PublicIdentityAVP,
                    "visited_network_identifier": VisitedNetworkIdentifierAVP,
    }

    optionals = {
                    # "drmp": DrmpAVP,
                    "destination_host": DestinationHostAVP,
                    # "oc_supported_features": OcSupportedFeaturesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "user_authorization_type": UserAuthorizationTypeAVP,
                    "uar_flags": UARFlagsAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 user_name=None,
                 oc_supported_features=None,
                 supported_features=None,
                 public_identity=None,
                 visited_network_identifier=None,
                 user_authorization_type=None,
                 uar_flags=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=USER_AUTHORIZATION_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterRequest._load(self, locals())


class ServerAssignmentAnswer(DiameterAnswer):
    """Implementation of Server-Assignment-Answer (SAA) command as per 
    clause 6.1.4 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Server-Assignment-Answer is indicated by the Command Code field set to 
    301 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import SAA
        >>> saa = SAA()
        >>> saa
        <Diameter Message: 301 [SAA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    # "drmp": DrmpAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "user_name": UserNameAVP,
                    # "oc_supported_features": OcSupportedFeaturesAVP,
                    # "oc_olr": OcOlrAVP,
                    # "load": LoadAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "user_data": UserDataAVP,
                    "charging_information": ChargingInformationAVP,
                    "associated_identities": AssociatedIdentitiesAVP,
                    "loose_route_information": LooseRouteInformationAVP,
                    "scscf_restoration_info": SCSCFRestorationInfoAVP,
                    "associated_registered_identities": AssociatedRegisteredIdentitiesAVP,
                    "server_name": ServerNameAVP,
                    "wildcarded_public_identity": WildcardedPublicIdentityAVP,
                    "priviledged_sender_indication": PriviledgedSenderIndicationAVP,
                    "allowed_waf_wwsf_identities": AllowedWAFWWSFIdentitiesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 supported_features=None,
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=SERVER_ASSIGNMENT_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterAnswer._load(self, locals())


class ServerAssignmentRequest(DiameterRequest):
    """Implementation of Server-Assignment-Request (SAR) command as per 
    clause 6.1.3 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Server-Assignment-Request is indicated by the Command Code field set to 
    301 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import SAR
        >>> sar_avps = {
        ...     "destination_realm": "example.com",
        ...     "destination_host": "host.example.com",
        ...     "user_name": "frodo"
        ... }
        >>> sar = SAR(**sar_avps)
        >>> sar
        <Diameter Message: 301 [SAR] REQ|PXY, 16777216 [3GPP Cx], 9 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "server_name": ServerNameAVP,
                    "server_assignment_type": ServerAssignmentTypeAVP,
                    "user_data_already_available": UserDataAlreadyAvailableAVP,
    }

    optionals = {
                    # "drmp": DrmpAVP,
                    "destination_host": DestinationHostAVP,
                    "user_name": UserNameAVP,
                    # "oc_supported_features": OcSupportedFeaturesAVP,
                    # "oc_olr": OcOlrAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "public_identity": PublicIdentityAVP,
                    "wildcarded_public_identity": WildcardedPublicIdentityAVP,
                    "scscf_restoration_info": SCSCFRestorationInfoAVP,
                    "multiple_registration_indication": MultipleRegistrationIndicationAVP,
                    "session_priority": SessionPriorityAVP,
                    "sar_flags": SARFlagsAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 user_name=None,
                 supported_features=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=SERVER_ASSIGNMENT_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterRequest._load(self, locals())


class LocationInfoAnswer(DiameterAnswer):
    """Implementation of Location-Info-Answer (LIA) command as per clause 6.1.6 of
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Location-Info-Answer is indicated by the Command Code field set to 302 and
    Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import LIA
        >>> lia = LIA()
        >>> lia
        <Diameter Message: 302 [LIA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    # "drmp": DrmpAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    # "oc_supported_features": OcSupportedFeaturesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "server_name": ServerNameAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "wildcarded_public_identity": WildcardedPublicIdentityAVP,
                    "lia_flags": LIAFlagsAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 oc_supported_features=None,
                 oc_olr=None,
                 load=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=LOCATION_INFO_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterAnswer._load(self, locals())


class LocationInfoRequest(DiameterRequest):
    """Implementation of Location-Info-Request (LIR) command as per clause 6.1.5 of 
    ETSI TS 129 272 V16.3.0 (2024-10).

    The Location-Info-Request is indicated by the Command Code field set to 302 and 
    the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import LIR
        >>> lir_avps = {
        ...     "destination_realm": "example.com",
        ...     "public_identity": "frodo",
        ... }
        >>> lir = LIR(**lir_avps)
        >>> lir
        <Diameter Message: 302 [LIR] REQ|PXY, 16777216 [3GPP Cx], 8 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "public_identity": PublicIdentityAVP,
    }

    optionals = {
                    # "drmp": DrmpAVP,
                    "destination_host": DestinationHostAVP,
                    # "oc_supported_features": OcSupportedFeaturesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "user_authorization_type": UserAuthorizationTypeAVP,
                    "session_priority": SessionPriorityAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 drmp=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 public_identity=None,
                 oc_supported_features=None,
                 supported_features=None,
                 user_authorization_type=None,
                 session_priority=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=LOCATION_INFO_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterRequest._load(self, locals())


class MultimediaAuthAnswer(DiameterAnswer):
    """Implementation of Multimedia-Auth-Answer (MAA) command as per clause 6.1.8 of
    ETSI TS 129 272 V16.3.0 (2024-10).

    The Multimedia-Auth-Answer is indicated by the Command Code field set to 303 and
    Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import MAA
        >>> maa = MAA()
        >>> maa
        <Diameter Message: 303 [MAA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    # "drmp": DrmpAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "user_name": UserNameAVP,
                    # "oc_supported_features": OcSupportedFeaturesAVP,
                    # "oc_olr": OcOlrAVP,
                    # "load": LoadAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "public_identity": PublicIdentityAVP,
                    "sip_number_auth_items": SIPNumberAuthItemsAVP,
                    "sip_auth_data_item": SIPAuthDataItemAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(),
                 destination_realm=None, 
                 oc_supported_features=None,
                 oc_olr=None,
                 load=None,
                 user_name=None,
                 supported_features=None,
                 public_identity=None,
                 sip_number_auth_items=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=MULTIMEDIA_AUTH_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterAnswer._load(self, locals())


class MultimediaAuthRequest(DiameterRequest):
    """Implementation of Multimedia-Auth-Request (MAR) command as per clause 6.1.7 of
    ETSI TS 129 229 V16.3.0 (2024-10).

    The Multimedia-Auth-Request is indicated by the Command Code field set to 303 and
    the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import MAR
        >>> mar_avps = {
        ...     "destination_realm": "example.com",
        ...     "public_identity": "frodo",
        ... }
        >>> mar = MAR(**mar_avps)
        >>> mar
        <Diameter Message: 303 [MAR] REQ|PXY, 16777216 [3GPP Cx], 8 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_name": UserNameAVP,
                    "public_identity": PublicIdentityAVP,
                    "sip_auth_data_item": SIPAuthDataItemAVP,
                    "sip_number_auth_items": SIPNumberAuthItemsAVP,
                    "server_name": ServerNameAVP
    }

    optionals = {
                    # "drmp": DrmpAVP,
                    "destination_host": DestinationHostAVP,
                    # "oc_supported_features": OcSupportedFeaturesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 user_name=None,
                 public_identity=None,
                 sip_auth_data_item=None,
                 sip_number_auth_items=None,
                 server_name=None,
                 oc_supported_features=None,
                 supported_features=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=MULTIMEDIA_AUTH_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterRequest._load(self, locals())


class RegistrationTerminationAnswer(DiameterAnswer):
    """Implementation of Registration-Termination-Answer (RTA) command as per 
    clause 6.1.10 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Registration-Termination-Answer is indicated by the Command Code field
    set to 304 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import RTA
        >>> rta = RTA()
        >>> rta
        <Diameter Message: 304 [RTA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    # "drmp": DrmpAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "associated_identities": AssociatedIdentitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "identity_with_emergency_registration": IdentityWithEmergencyRegistrationAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 supported_features=None,
                 associated_identities=None,
                 identity_with_emergency_registration=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=REGISTRATION_TERMINATION_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterAnswer._load(self, locals())


class RegistrationTerminationRequest(DiameterRequest):
    """Implementation of Registration-Termination-Request (RTR) command as per 
    clause 6.1.10 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Registration-Termination-Request is indicated by the Command Code field set to 
    304 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import RTR
        >>> rtr_avps = {
        ...     "destination_realm": "example.com",
        ...     "user_name": "frodo",
        ... }
        >>> rtr = RTR(**rtr_avps)
        >>> rtr
        <Diameter Message: 304 [RTR] REQ|PXY, 16777216 [3GPP Cx], 10 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_name": UserNameAVP,
                    "deregistration_reason": DeregistrationReasonAVP,
    }

    optionals = {
                    # "drmp": DrmpAVP,
                    "associated_identities": AssociatedIdentitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "public_identity": PublicIdentityAVP,
                    "rtr_flags": RTRFlagsAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_realm=None,
                 user_name=None,
                 supported_features=None,
                 deregistration_reason=None,
                 rtr_flags=None,
                 public_identity=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=REGISTRATION_TERMINATION_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterRequest._load(self, locals())


class PushProfileAnswer(DiameterAnswer):
    """Implementation of Push-Profile-Answer (PPA) command as per 
    clause 6.1.12 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Push-Profile-Answer is indicated by the Command Code field
    set to 305 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import PPA
        >>> ppa = PPA()
        >>> ppa
        <Diameter Message: 305 [PPA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    # "drmp": DrmpAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "associated_identities": AssociatedIdentitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "identity_with_emergency_registration": IdentityWithEmergencyRegistrationAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 supported_features=None,
                 associated_identities=None,
                 identity_with_emergency_registration=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=PUSH_PROFILE_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterAnswer._load(self, locals())


class PushProfileRequest(DiameterRequest):
    """Implementation of Push-Profile-Request (PPR) command as per 
    clause 6.1.11 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Push-Profile-Request is indicated by the Command Code field
    set to 305 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import PPR
        >>> ppr_avps = {
        ...     "destination_realm": "example.com",
        ...     "user_name": "frodo",
        ... }
        >>> ppr = PPR(**ppr_avps)
        >>> ppr
        <Diameter Message: 305 [PPR] REQ|PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    # "drmp": DrmpAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "associated_identities": AssociatedIdentitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx_Dx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                command_code=PUSH_PROFILE_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx_Dx)

        DiameterRequest._load(self, locals())

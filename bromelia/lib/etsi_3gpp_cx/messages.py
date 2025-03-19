# -*- coding: utf-8 -*-
"""
    bromelia.lib.etsi_3gpp_cx.messages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the Diameter protocol messages for 3GPP Cx
    Application Id.

    :copyright: (c) 2020-present Roch-Alexandre Nomine
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
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "server_name": ServerNameAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 server_name=None,
                 server_capabilities=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=USER_AUTHORIZATION_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx)

        DiameterAnswer._load(self, locals())


class UserAuthorizationRequest(DiameterRequest):
    """Implementation of User-Authorization-Request (UAR) command as per 
    clause 6.1.1 of ETSI TS 129 229 V16.3.0 (2024-10).

    The User-Authorization-Request is indicated by the Command Code field
    set to 300 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import UAR
        >>> uar_avps = {
        ...     "destination_realm": "example.com",
        ...     "user_name": "frodo",
        ...     "public_identity": "sip:frodo@example.com",
        ...     "server_name": "server.example.com"
        ... }
        >>> uar = UAR(**uar_avps)
        >>> uar
        <Diameter Message: 300 [UAR] REQ|PXY, 16777216 [3GPP Cx], 8 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_name": UserNameAVP,
                    "public_identity": PublicIdentityAVP,
                    "server_name": ServerNameAVP,
    }

    optionals = {
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "destination_host": DestinationHostAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 user_name=None,
                 public_identity=None,
                 server_name=None,
                 supported_features=None,
                 server_capabilities=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=USER_AUTHORIZATION_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx)

        DiameterRequest._load(self, locals())


class ServerAssignmentAnswer(DiameterAnswer):
    """Implementation of Server-Assignment-Answer (SAA) command as per 
    clause 6.1.4 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Server-Assignment-Answer is indicated by the Command Code field
    set to 301 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import SAA
        >>> saa = SAA()
        >>> saa
        <Diameter Message: 301 [SAA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "server_name": ServerNameAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 server_name=None,
                 server_capabilities=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=SERVER_ASSIGNMENT_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx)

        DiameterAnswer._load(self, locals())


class ServerAssignmentRequest(DiameterRequest):
    """Implementation of Server-Assignment-Request (SAR) command as per 
    clause 6.1.3 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Server-Assignment-Request is indicated by the Command Code field
    set to 301 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import SAR
        >>> sar_avps = {
        ...     "destination_realm": "example.com",
        ...     "user_name": "frodo",
        ...     "server_name": "server.example.com",
        ...     "server_assignment_type": SERVER_ASSIGNMENT_TYPE_REGISTRATION
        ... }
        >>> sar = SAR(**sar_avps)
        >>> sar
        <Diameter Message: 301 [SAR] REQ|PXY, 16777216 [3GPP Cx], 9 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_name": UserNameAVP,
                    "server_name": ServerNameAVP,
                    "server_assignment_type": ServerAssignmentTypeAVP,
    }

    optionals = {
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "destination_host": DestinationHostAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 user_name=None,
                 server_name=None,
                 server_assignment_type=None,
                 supported_features=None,
                 server_capabilities=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=SERVER_ASSIGNMENT_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx)

        DiameterRequest._load(self, locals())


class LocationInfoAnswer(DiameterAnswer):
    """Implementation of Location-Info-Answer (LIA) command as per 
    clause 6.1.6 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Location-Info-Answer is indicated by the Command Code field
    set to 302 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import LIA
        >>> lia = LIA()
        >>> lia
        <Diameter Message: 302 [LIA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "server_name": ServerNameAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 server_name=None,
                 server_capabilities=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=LOCATION_INFO_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx)

        DiameterAnswer._load(self, locals())


class LocationInfoRequest(DiameterRequest):
    """Implementation of Location-Info-Request (LIR) command as per 
    clause 6.1.5 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Location-Info-Request is indicated by the Command Code field
    set to 302 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import LIR
        >>> lir_avps = {
        ...     "destination_realm": "example.com",
        ...     "public_identity": "sip:frodo@example.com"
        ... }
        >>> lir = LIR(**lir_avps)
        >>> lir
        <Diameter Message: 302 [LIR] REQ|PXY, 16777216 [3GPP Cx], 7 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "public_identity": PublicIdentityAVP,
    }

    optionals = {
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "destination_host": DestinationHostAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 public_identity=None,
                 supported_features=None,
                 server_capabilities=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=LOCATION_INFO_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx)

        DiameterRequest._load(self, locals())


class MultimediaAuthAnswer(DiameterAnswer):
    """Implementation of Multimedia-Auth-Answer (MAA) command as per 
    clause 6.1.8 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Multimedia-Auth-Answer is indicated by the Command Code field
    set to 303 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import MAA
        >>> maa = MAA()
        >>> maa
        <Diameter Message: 303 [MAA] PXY, 16777216 [3GPP Cx], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "server_name": ServerNameAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 server_name=None,
                 server_capabilities=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self, 
                                command_code=MULTIMEDIA_AUTH_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx)

        DiameterAnswer._load(self, locals())


class MultimediaAuthRequest(DiameterRequest):
    """Implementation of Multimedia-Auth-Request (MAR) command as per 
    clause 6.1.7 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Multimedia-Auth-Request is indicated by the Command Code field
    set to 303 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import MAR
        >>> mar_avps = {
        ...     "destination_realm": "example.com",
        ...     "user_name": "frodo",
        ...     "public_identity": "sip:frodo@example.com",
        ...     "server_name": "server.example.com"
        ... }
        >>> mar = MAR(**mar_avps)
        >>> mar
        <Diameter Message: 303 [MAR] REQ|PXY, 16777216 [3GPP Cx], 8 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_name": UserNameAVP,
                    "public_identity": PublicIdentityAVP,
                    "server_name": ServerNameAVP,
    }

    optionals = {
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "destination_host": DestinationHostAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "server_capabilities": ServerCapabilitiesAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 user_name=None,
                 public_identity=None,
                 server_name=None,
                 supported_features=None,
                 server_capabilities=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=MULTIMEDIA_AUTH_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx)

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
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = { 
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
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

        DiameterAnswer.__init__(self, 
                                command_code=REGISTRATION_TERMINATION_MESSAGE, 
                                application_id=DIAMETER_APPLICATION_Cx)

        DiameterAnswer._load(self, locals())


class RegistrationTerminationRequest(DiameterRequest):
    """Implementation of Registration-Termination-Request (RTR) command as per 
    clause 6.1.9 of ETSI TS 129 229 V16.3.0 (2024-10).

    The Registration-Termination-Request is indicated by the Command Code field
    set to 304 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_cx import RTR
        >>> rtr_avps = {
        ...     "destination_realm": "example.com",
        ...     "public_identity": "sip:frodo@example.com",
        ...     "deregistration_reason": DEREGISTRATION_REASON_PERMANENT_TERMINATION
        ... }
        >>> rtr = RTR(**rtr_avps)
        >>> rtr
        <Diameter Message: 304 [RTR] REQ|PXY, 16777216 [3GPP Cx], 7 AVP(s)>
    """    

    mandatory = {
                    "session_id": SessionIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "public_identity": PublicIdentityAVP,
                    "deregistration_reason": DeregistrationReasonAVP,
    }

    optionals = {
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "destination_host": DestinationHostAVP,
                    "supported_features": SupportedFeaturesAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self, 
                 session_id=platform.node(), 
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Cx)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(), 
                 origin_realm=socket.getfqdn(), 
                 destination_host=None,
                 destination_realm=None,
                 public_identity=None,
                 deregistration_reason=None,
                 supported_features=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self, 
                                 command_code=REGISTRATION_TERMINATION_MESSAGE, 
                                 application_id=DIAMETER_APPLICATION_Cx)

        DiameterRequest._load(self, locals())

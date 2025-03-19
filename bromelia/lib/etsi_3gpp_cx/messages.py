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

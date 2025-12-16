# -*- coding: utf-8 -*-
"""
    bromelia.lib.etsi_3gpp_sh.messages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains Diameter message classes for the Sh interface
    as per 3GPP TS 29.329.

    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

import platform
import socket

from ...base import DiameterAnswer, DiameterRequest
from ...avps.ietf.rfc6733 import *
from ...constants.ietf.rfc6733 import *
from ...constants.app_ids import DIAMETER_APPLICATION_Sh
from ...constants.etsi_3gpp.ts_129_329 import *
from .avps import *


class ProfileUpdateAnswer(DiameterAnswer):
    """Implementation of Profile-Update-Answer (PUA) command as per
    clause 6.1.4 of ETSI TS 129 329 V15.1.0 (2018-07).

    The Profile-Update-Answer is indicated by the Command Code field set to
    307 and Command Flag's 'R' bit cleared.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_sh import PUA
        >>> pua = PUA()
        >>> pua
        <Diameter Message: 307 [PUA] PXY, 16777217 [3GPP Sh], 5 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = {
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 user_name=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self,
                                command_code=PROFILE_UPDATE_MESSAGE,
                                application_id=DIAMETER_APPLICATION_Sh)

        DiameterAnswer._load(self, locals())


class ProfileUpdateRequest(DiameterRequest):
    """Implementation of Profile-Update-Request (PUR) command as per
    clause 6.1.3 of ETSI TS 129 329 V15.1.0 (2018-07).

    The Profile-Update-Request is indicated by the Command Code
    field set to 307 and the 'R' bit set in the Command Flags field.

    Usage::

        >>> from bromelia.lib.etsi_3gpp_sh import PUR
        >>> from bromelia.lib.etsi_3gpp_sh import UserIdentityAVP, DataReferenceAVP, UserDataAVP
        >>> from bromelia.avps.etsi_3gpp.ts_129_229 import PublicIdentityAVP
        >>> pur_avps = {
        ...     "destination_realm": "example.com",
        ...     "user_identity": UserIdentityAVP([PublicIdentityAVP("sip:user@example.com")]),
        ...     "data_reference": DataReferenceAVP(DATA_REFERENCE_REPOSITORY_DATA),
        ...     "user_data": UserDataAVP(b"<xml>...</xml>")
        ... }
        >>> pur = PUR(**pur_avps)
        >>> pur
        <Diameter Message: 307 [PUR] REQ PXY, 16777217 [3GPP Sh], 9 AVP(s)>
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_identity": UserIdentityAVP,
                    "data_reference": DataReferenceAVP,
                    "user_data": UserDataAVP,
    }

    optionals = {
                    "destination_host": DestinationHostAVP,
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 drmp=None,
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 destination_host=None,
                 destination_realm=None,
                 user_identity=None,
                 data_reference=None,
                 user_data=None,
                 user_name=None,
                 supported_features=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self,
                                 command_code=PROFILE_UPDATE_MESSAGE,
                                 application_id=DIAMETER_APPLICATION_Sh)

        DiameterRequest._load(self, locals())


class UserDataAnswer(DiameterAnswer):
    """Implementation of User-Data-Answer (UDA) command as per
    clause 6.1.2 of ETSI TS 129 329 V15.1.0 (2018-07).

    The User-Data-Answer is indicated by the Command Code field set to
    306 and Command Flag's 'R' bit cleared.
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = {
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "user_data": UserDataAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 user_name=None,
                 supported_features=None,
                 user_data=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self,
                                command_code=USER_DATA_MESSAGE,
                                application_id=DIAMETER_APPLICATION_Sh)

        DiameterAnswer._load(self, locals())


class UserDataRequest(DiameterRequest):
    """Implementation of User-Data-Request (UDR) command as per
    clause 6.1.1 of ETSI TS 129 329 V15.1.0 (2018-07).

    The User-Data-Request is indicated by the Command Code
    field set to 306 and the 'R' bit set in the Command Flags field.
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_identity": UserIdentityAVP,
                    "data_reference": DataReferenceAVP,
    }

    optionals = {
                    "destination_host": DestinationHostAVP,
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "service_indication": ServiceIndicationAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 destination_host=None,
                 destination_realm=None,
                 user_identity=None,
                 data_reference=None,
                 user_name=None,
                 supported_features=None,
                 service_indication=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self,
                                 command_code=USER_DATA_MESSAGE,
                                 application_id=DIAMETER_APPLICATION_Sh)

        DiameterRequest._load(self, locals())


class SubscribeNotificationsAnswer(DiameterAnswer):
    """Implementation of Subscribe-Notifications-Answer (SNA) command as per
    clause 6.1.6 of ETSI TS 129 329 V15.1.0 (2018-07).

    The Subscribe-Notifications-Answer is indicated by the Command Code field set to
    308 and Command Flag's 'R' bit cleared.
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = {
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "user_data": UserDataAVP,
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 user_name=None,
                 supported_features=None,
                 user_data=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self,
                                command_code=SUBSCRIBE_NOTIFICATIONS_MESSAGE,
                                application_id=DIAMETER_APPLICATION_Sh)

        DiameterAnswer._load(self, locals())


class SubscribeNotificationsRequest(DiameterRequest):
    """Implementation of Subscribe-Notifications-Request (SNR) command as per
    clause 6.1.5 of ETSI TS 129 329 V15.1.0 (2018-07).

    The Subscribe-Notifications-Request is indicated by the Command Code
    field set to 308 and the 'R' bit set in the Command Flags field.
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_identity": UserIdentityAVP,
                    "data_reference": DataReferenceAVP,
    }

    optionals = {
                    "destination_host": DestinationHostAVP,
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "service_indication": ServiceIndicationAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 destination_host=None,
                 destination_realm=None,
                 user_identity=None,
                 data_reference=None,
                 user_name=None,
                 supported_features=None,
                 service_indication=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self,
                                 command_code=SUBSCRIBE_NOTIFICATIONS_MESSAGE,
                                 application_id=DIAMETER_APPLICATION_Sh)

        DiameterRequest._load(self, locals())


class PushNotificationAnswer(DiameterAnswer):
    """Implementation of Push-Notification-Answer (PNA) command as per
    clause 6.1.8 of ETSI TS 129 329 V15.1.0 (2018-07).

    The Push-Notification-Answer is indicated by the Command Code field set to
    309 and Command Flag's 'R' bit cleared.
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
    }

    optionals = {
                    "result_code": ResultCodeAVP,
                    "experimental_result": ExperimentalResultAVP,
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "failed_avp": FailedAvpAVP,
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 result_code=None,
                 experimental_result=None,
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 user_name=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterAnswer.__init__(self,
                                command_code=PUSH_NOTIFICATION_MESSAGE,
                                application_id=DIAMETER_APPLICATION_Sh)

        DiameterAnswer._load(self, locals())


class PushNotificationRequest(DiameterRequest):
    """Implementation of Push-Notification-Request (PNR) command as per
    clause 6.1.7 of ETSI TS 129 329 V15.1.0 (2018-07).

    The Push-Notification-Request is indicated by the Command Code
    field set to 309 and the 'R' bit set in the Command Flags field.
    """

    mandatory = {
                    "session_id": SessionIdAVP,
                    "vendor_specific_application_id": VendorSpecificApplicationIdAVP,
                    "auth_session_state": AuthSessionStateAVP,
                    "origin_host": OriginHostAVP,
                    "origin_realm": OriginRealmAVP,
                    "destination_host": DestinationHostAVP,
                    "destination_realm": DestinationRealmAVP,
                    "user_identity": UserIdentityAVP,
                    "user_data": UserDataAVP,
    }

    optionals = {
                    "user_name": UserNameAVP,
                    "supported_features": "SupportedFeaturesAVP",
                    "proxy_info": ProxyInfoAVP,
                    "route_record": RouteRecordAVP,
    }

    def __init__(self,
                 session_id=platform.node(),
                 vendor_specific_application_id=[VendorIdAVP(VENDOR_ID_3GPP), AuthApplicationIdAVP(DIAMETER_APPLICATION_Sh)],
                 auth_session_state=NO_STATE_MAINTAINED,
                 origin_host=platform.node(),
                 origin_realm=socket.getfqdn(),
                 destination_host=None,
                 destination_realm=None,
                 user_identity=None,
                 user_data=None,
                 user_name=None,
                 supported_features=None,
                 proxy_info=None,
                 route_record=None,
                 **kwargs):

        DiameterRequest.__init__(self,
                                 command_code=PUSH_NOTIFICATION_MESSAGE,
                                 application_id=DIAMETER_APPLICATION_Sh)

        DiameterRequest._load(self, locals())

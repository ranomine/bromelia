# -*- coding: utf-8 -*-
"""
    bromelia.constants.etsi_3gpp.ts_129_329
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains constants defined in ETSI TS 129 329 (Sh interface).

    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ..._internal_utils import convert_to_3_bytes
from ..._internal_utils import convert_to_4_bytes


#: Diameter Command Codes for Sh interface (3GPP TS 29.329)
USER_DATA_MESSAGE = convert_to_3_bytes(306)
PROFILE_UPDATE_MESSAGE = convert_to_3_bytes(307)
SUBSCRIBE_NOTIFICATIONS_MESSAGE = convert_to_3_bytes(308)
PUSH_NOTIFICATION_MESSAGE = convert_to_3_bytes(309)

#: Diameter AVPs for Sh interface
#: Using SH_ prefix to avoid conflicts with Cx constants
SH_USER_IDENTITY_AVP_CODE = convert_to_4_bytes(700)
SH_MSISDN_AVP_CODE = convert_to_4_bytes(701)
SH_USER_DATA_AVP_CODE = convert_to_4_bytes(702)
SH_DATA_REFERENCE_AVP_CODE = convert_to_4_bytes(703)
SH_SERVICE_INDICATION_AVP_CODE = convert_to_4_bytes(704)
SUBS_REQ_TYPE_AVP_CODE = convert_to_4_bytes(705)
REQUESTED_DOMAIN_AVP_CODE = convert_to_4_bytes(706)
CURRENT_LOCATION_AVP_CODE = convert_to_4_bytes(707)
IDENTITY_SET_AVP_CODE = convert_to_4_bytes(708)
EXPIRY_TIME_AVP_CODE = convert_to_4_bytes(709)
SEND_DATA_INDICATION_AVP_CODE = convert_to_4_bytes(710)

#: Data-Reference values (AVP Code 703)
DATA_REFERENCE_REPOSITORY_DATA = convert_to_4_bytes(0)
DATA_REFERENCE_IMS_PUBLIC_IDENTITY = convert_to_4_bytes(10)
DATA_REFERENCE_IMS_USER_STATE = convert_to_4_bytes(11)
DATA_REFERENCE_S_CSCF_NAME = convert_to_4_bytes(12)
DATA_REFERENCE_INITIAL_FILTER_CRITERIA = convert_to_4_bytes(13)
DATA_REFERENCE_LOCATION_INFORMATION = convert_to_4_bytes(14)
DATA_REFERENCE_USER_STATE = convert_to_4_bytes(15)
DATA_REFERENCE_CHARGING_INFORMATION = convert_to_4_bytes(16)
DATA_REFERENCE_MSISDN = convert_to_4_bytes(17)
DATA_REFERENCE_PSI_ACTIVATION = convert_to_4_bytes(18)
DATA_REFERENCE_DSAI = convert_to_4_bytes(19)
DATA_REFERENCE_ALIASES_REPOSITORY_DATA = convert_to_4_bytes(20)
DATA_REFERENCE_SERVICE_LEVEL_TRACE_INFO = convert_to_4_bytes(21)
DATA_REFERENCE_IP_ADDRESS_SECURE_BINDING_INFO = convert_to_4_bytes(22)
DATA_REFERENCE_SERVICE_PRIORITY_LEVEL = convert_to_4_bytes(23)
DATA_REFERENCE_SMS_REGISTRATION_INFO = convert_to_4_bytes(24)
DATA_REFERENCE_SERVED_USER_IDENTITY = convert_to_4_bytes(25)
DATA_REFERENCE_IMSI = convert_to_4_bytes(26)
DATA_REFERENCE_IMS_USER_STATE_EPS = convert_to_4_bytes(27)
DATA_REFERENCE_MSISDN_MAPPINGS = convert_to_4_bytes(28)
DATA_REFERENCE_STN_SR = convert_to_4_bytes(29)
DATA_REFERENCE_CSRN = convert_to_4_bytes(30)

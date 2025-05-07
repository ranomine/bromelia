# -*- coding: utf-8 -*-
"""
    bromelia.constants.etsi_3gpp.ts_129_229
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains constants defined in ETSI TS 129 229.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ..._internal_utils import convert_to_3_bytes
from ..._internal_utils import convert_to_4_bytes

#: Diameter Messages
USER_AUTHORIZATION_MESSAGE = convert_to_3_bytes(300)
SERVER_ASSIGNMENT_MESSAGE = convert_to_3_bytes(301)
LOCATION_INFO_MESSAGE = convert_to_3_bytes(302)
MULTIMEDIA_AUTH_MESSAGE = convert_to_3_bytes(303)
REGISTRATION_TERMINATION_MESSAGE = convert_to_3_bytes(304)
PUSH_PROFILE_MESSAGE = convert_to_3_bytes(305)

#: Diameter AVPs
VISITED_NETWORK_IDENTIFIER_AVP_CODE = convert_to_4_bytes(600)
PUBLIC_IDENTITY_AVP_CODE = convert_to_4_bytes(601)
SERVER_NAME_AVP_CODE = convert_to_4_bytes(602)
SERVER_CAPABILITIES_AVP_CODE = convert_to_4_bytes(603)
MANDATORY_CAPABILITY_AVP_CODE = convert_to_4_bytes(604)
OPTIONAL_CAPABILITY_AVP_CODE = convert_to_4_bytes(605)
USER_DATA_AVP_CODE = convert_to_4_bytes(606)
SIP_NUMBER_AUTH_ITEMS_AVP_CODE = convert_to_4_bytes(607)
SIP_AUTHENTICATION_SCHEME_AVP_CODE = convert_to_4_bytes(608)
SIP_AUTHENTICATE_AVP_CODE = convert_to_4_bytes(609)
SIP_AUTHORIZATION_AVP_CODE = convert_to_4_bytes(610)
SIP_AUTHENTICATION_CTX_CODE = convert_to_4_bytes(611)
SIP_AUTH_DATA_ITEM_AVP_CODE = convert_to_4_bytes(612)
SERVER_ASSIGNMENT_TYPE_AVP_CODE = convert_to_4_bytes(614)
REASON_CODE_AVP_CODE = convert_to_4_bytes(616)
DE_REGISTRATION_REASON_AVP_CODE = convert_to_4_bytes(615)
REASON_INFO_AVP_CODE = convert_to_4_bytes(617)
CHARGING_INFORMATION_AVP_CODE = convert_to_4_bytes(618)
PRIMARY_EVENT_CHARGING_FUNCTION_NAME_AVP_CODE = convert_to_4_bytes(619)
SECONDARY_EVENT_CHARGING_FUNCTION_NAME_AVP_CODE = convert_to_4_bytes(620)
PRIMARY_CHARGING_COLLECTION_FUNCTION_NAME_AVP_CODE = convert_to_4_bytes(621)
SECONDARY_CHARGING_COLLECTION_FUNCTION_NAME_AVP_CODE = convert_to_4_bytes(622)
USER_AUTHORIZATION_TYPE_AVP_CODE = convert_to_4_bytes(623)
USER_DATA_ALREADY_AVAILABLE_AVP_CODE = convert_to_4_bytes(624)
CONFIDENTIALITY_KEY_AVP_CODE = convert_to_4_bytes(625)
INTEGRITY_KEY_AVP_CODE = convert_to_4_bytes(626)
SUPPORTED_FEATURES_AVP_CODE = convert_to_4_bytes(628)
FEATURE_LIST_ID_AVP_CODE = convert_to_4_bytes(629)
FEATURE_LIST_AVP_CODE = convert_to_4_bytes(630)
SUPPORTED_APPLICATIONS_AVP_CODE = convert_to_4_bytes(631)
ASSOCIATED_IDENTITIES_AVP_CODE = convert_to_4_bytes(632)
ORIGINATING_REQUEST_AVP_CODE = convert_to_4_bytes(633)
WILDCARDED_PUBLIC_IDENTITY_AVP_CODE = convert_to_4_bytes(634)
SIP_DIGEST_AUTHENTICATE_AVP_CODE = convert_to_4_bytes(635)
UAR_FLAGS_AVP_CODE = convert_to_4_bytes(637)
LOOSE_ROUTE_INDICATION_AVP_CODE = convert_to_4_bytes(638)
SCSCF_RESTORATION_INFO_AVP_CODE = convert_to_4_bytes(639)
PATH_AVP_CODE = convert_to_4_bytes(640)
CONTACT_AVP_CODE = convert_to_4_bytes(641)
SUBSCRIPTION_INFO_AVP_CODE = convert_to_4_bytes(642)
CALL_ID_SIP_HEADER_AVP_CODE = convert_to_4_bytes(643)
FROM_SIP_HEADER_AVP_CODE = convert_to_4_bytes(644)
TO_SIP_HEADER_AVP_CODE = convert_to_4_bytes(645)
RECORD_ROUTE_AVP_CODE = convert_to_4_bytes(646)
ASSOCIATED_REGISTERED_IDENTITIES_AVP_CODE = convert_to_4_bytes(647)
MULTIPLE_REGISTRATION_INDICATION_AVP_CODE = convert_to_4_bytes(648)
RESTORATION_INFO_AVP_CODE = convert_to_4_bytes(649)
SESSION_PRIORITY_AVP_CODE = convert_to_4_bytes(650)
IDENTITY_WITH_EMERGENCY_REGISTRATION_AVP_CODE = convert_to_4_bytes(651)
PRIVILEDGED_SENDER_INDICATION_AVP_CODE = convert_to_4_bytes(652)
LIA_FLAGS_AVP_CODE = convert_to_4_bytes(653)
INITIAL_CSEQ_SEQUENCE_NUMBER_AVP_CODE = convert_to_4_bytes(654)
SAR_FLAGS_AVP_CODE = convert_to_4_bytes(655)
ALLOWED_WAF_WWSF_IDENTITIES_AVP_CODE = convert_to_4_bytes(656)
WEBRTC_AUTHENTICATION_FUNCTION_NAME_AVP_CODE = convert_to_4_bytes(657)
WEBRTC_WEB_SERVER_NAME_AVP_CODE = convert_to_4_bytes(658)
RTR_FLAGS_AVP_CODE = convert_to_4_bytes(659)
P_CSCF_SUBSCRIPTION_INFO_AVP_CODE = convert_to_4_bytes(660)
REGISTRATION_TIME_OUT_AVP_CODE = convert_to_4_bytes(661)



#: List of Reason-Code AVP values.
#: For more information, please refer to Section 6.3.17 of 
#: ETSI TS 129 229 V11.3.0 (2013-04).
REASON_CODE_PERMANENT_TERMINATION = convert_to_4_bytes(0)
REASON_CODE_NEW_SERVER_ASSIGNED = convert_to_4_bytes(1)
REASON_CODE_SERVER_CHANGE = convert_to_4_bytes(2)
REASON_CODE_REMOVE_CHANGE = convert_to_4_bytes(3)

#: List of Feature-List-ID AVP values.
#: For more information, please refer to Section 6.3.30 of 
#: ETSI TS 129 229 V14.3.0 (2019-10).
FEATURE_LIST_ID_1 = convert_to_4_bytes(1)
FEATURE_LIST_ID_2 = convert_to_4_bytes(2)

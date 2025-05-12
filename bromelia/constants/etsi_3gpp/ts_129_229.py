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
SIP_ITEM_NUMBER_AVP_CODE = convert_to_4_bytes(613)
SERVER_ASSIGNMENT_TYPE_AVP_CODE = convert_to_4_bytes(614)
REASON_CODE_AVP_CODE = convert_to_4_bytes(616)
DEREGISTRATION_REASON_AVP_CODE = convert_to_4_bytes(615)
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
WEBRTC_WEB_SERVER_FUNCTION_NAME_AVP_CODE = convert_to_4_bytes(658)
RTR_FLAGS_AVP_CODE = convert_to_4_bytes(659)
P_CSCF_SUBSCRIPTION_INFO_AVP_CODE = convert_to_4_bytes(660)
REGISTRATION_TIME_OUT_AVP_CODE = convert_to_4_bytes(661)



#: List of Reason-Code AVP values.
#: For more information, please refer to Section 6.3.17 of 
#: ETSI TS 129 229 V11.3.0 (2013-04).
REASON_CODE_PERMANENT_TERMINATION = convert_to_4_bytes(0)
REASON_CODE_NEW_SERVER_ASSIGNED = convert_to_4_bytes(1)
REASON_CODE_SERVER_CHANGE = convert_to_4_bytes(2)
REASON_CODE_REMOVE_S_CSCF = convert_to_4_bytes(3)

#: List of User-Authorization-Type AVP values.
#: For more information, please refer to Section 6.3.24 of 
#: ETSI TS 129 229 V16.3.0 (2024-10).
USER_AUTHORIZATION_TYPE_REGISTRATION = convert_to_4_bytes(0)
USER_AUTHORIZATION_TYPE_DE_REGISTRATION = convert_to_4_bytes(1)
USER_AUTHORIZATION_TYPE_REGISTRATION_AND_CAPABILITIES = convert_to_4_bytes(2)

#: List of User-Data-Already-Available AVP values.
#: For more information, please refer to Section 6.3.26 of 
#: ETSI TS 129 229 V16.3.0 (2024-10).
USER_DATA_ALREADY_AVAILABLE_USER_DATA_NOT_AVAILABLE = convert_to_4_bytes(0)
USER_DATA_ALREADY_AVAILABLE_USER_DATA_ALREADY_AVAILABLE = convert_to_4_bytes(1)

#: List of Loose-Route-Indication AVP values.
#: For more information, please refer to Section 6.3.45 of 
#: ETSI TS 129 229 V16.3.0 (2024-10).
LOOSE_ROUTE_INDICATION_LOOSE_ROUTE_NOT_REQUIRED = convert_to_4_bytes(0)
LOOSE_ROUTE_INDICATION_LOOSE_ROUTE_REQUIRED = convert_to_4_bytes(1)

#: List of Multiple-Registration-Indication AVP values.
#: For more information, please refer to Section 6.3.51 of 
#: ETSI TS 129 229 V16.3.0 (2024-10).
MULTIPLE_REGISTRATION_INDICATION_NOT_MULTIPLE_REGISTRATION= convert_to_4_bytes(0)
MULTIPLE_REGISTRATION_INDICATION_MULTIPLE_REGISTRATION= convert_to_4_bytes(1)

#: List of Session-Priority AVP values.
#: For more information, please refer to Section 6.3.56 of 
#: ETSI TS 129 229 V16.3.0 (2024-10).
SESSION_PRIORITY_PRIORITY_0 = convert_to_4_bytes(0)
SESSION_PRIORITY_PRIORITY_1 = convert_to_4_bytes(1)
SESSION_PRIORITY_PRIORITY_2 = convert_to_4_bytes(2)
SESSION_PRIORITY_PRIORITY_3 = convert_to_4_bytes(3)
SESSION_PRIORITY_PRIORITY_4 = convert_to_4_bytes(4)

#: List of Priviledged-Sender-Indication AVP values.
#: For more information, please refer to Section 6.3.58 of 
#: ETSI TS 129 229 V16.3.0 (2024-10).
PRIVILEDGED_SENDER_INDICATION_NOT_PRIVILEDGED_SENDER = convert_to_4_bytes(0)
PRIVILEDGED_SENDER_INDICATION_PRIVILEDGED_SENDER = convert_to_4_bytes(1)

#: List of Originating-Request AVP values.
#: For more information, please refer to Section 6.3.34 of 
#: ETSI TS 129 229 V16.3.0 (2024-10).
ORIGINATING_REQUEST_ORIGINATING = convert_to_4_bytes(0)

#: List of Feature-List-ID AVP values.
#: For more information, please refer to Section 6.3.30 of 
#: ETSI TS 129 229 V14.3.0 (2019-10).
FEATURE_LIST_ID_1 = convert_to_4_bytes(1)
FEATURE_LIST_ID_2 = convert_to_4_bytes(2)

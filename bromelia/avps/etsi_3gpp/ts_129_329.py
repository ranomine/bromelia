# -*- coding: utf-8 -*-
"""
    bromelia.etsi_3gpp.ts_129_329
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains Diameter AVP classes defined in ETSI TS 129 329 (Sh interface).

    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ...base import DiameterAVP
from ...constants.etsi_3gpp.ts_129_329 import *
from ...constants.ietf.rfc6733 import VENDOR_ID_3GPP
from ...types import *
from ...utils import decode_from_tbcd, encode_to_tbcd

# Export Sh-specific AVPs, excluding UserDataAVP to avoid conflict with Cx UserDataAVP (code 606)
# Sh UserDataAVP can still be imported explicitly when needed
__all__ = [
    "UserIdentityAVP",
    "MsisdnAVP",
    "DataReferenceAVP",
    "ServiceIndicationAVP",
]


class UserIdentityAVP(DiameterAVP, GroupedType):
    """Implementation of User-Identity AVP in Section 6.3.1 of
    ETSI TS 129 329 V15.1.0 (2018-07).

    The User-Identity AVP (AVP Code 700) is of type Grouped.
    """
    code = SH_USER_IDENTITY_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    mandatory = {}
    optionals = {
                    "public_identity": "PublicIdentityAVP",
                    "msisdn": "MsisdnAVP",
    }

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             UserIdentityAVP.code,
                             UserIdentityAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        GroupedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class MsisdnAVP(DiameterAVP, OctetStringType):
    """Implementation of MSISDN AVP in Section 6.3.2 of
    ETSI TS 129 329 V15.1.0 (2018-07).

    The MSISDN AVP (AVP Code 701) is of type OctetString.
    """
    code = SH_MSISDN_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             MsisdnAVP.code,
                             MsisdnAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=self.encode(data), vendor_id=VENDOR_ID_3GPP)


    def encode(self, data):
        if isinstance(data, int):
            return bytes.fromhex(encode_to_tbcd(data))

        elif isinstance(data, str):
            return bytes.fromhex(encode_to_tbcd(int(data)))

        elif isinstance(data, bytes):
            return data


    def decode(self):
        return decode_from_tbcd(self.data)


class UserDataAVP(DiameterAVP, OctetStringType):
    """Implementation of User-Data AVP in Section 6.3.3 of
    ETSI TS 129 329 V15.1.0 (2018-07).

    The User-Data AVP (AVP Code 702) is of type OctetString.
    """
    code = SH_USER_DATA_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             UserDataAVP.code,
                             UserDataAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class DataReferenceAVP(DiameterAVP, EnumeratedType):
    """Implementation of Data-Reference AVP in Section 6.3.4 of
    ETSI TS 129 329 V15.1.0 (2018-07).

    The Data-Reference AVP (AVP Code 703) is of type Enumerated.
    """
    code = SH_DATA_REFERENCE_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    values = [
        DATA_REFERENCE_REPOSITORY_DATA,
        DATA_REFERENCE_IMS_PUBLIC_IDENTITY,
        DATA_REFERENCE_IMS_USER_STATE,
        DATA_REFERENCE_S_CSCF_NAME,
        DATA_REFERENCE_INITIAL_FILTER_CRITERIA,
        DATA_REFERENCE_LOCATION_INFORMATION,
        DATA_REFERENCE_USER_STATE,
        DATA_REFERENCE_CHARGING_INFORMATION,
        DATA_REFERENCE_MSISDN,
        DATA_REFERENCE_PSI_ACTIVATION,
        DATA_REFERENCE_DSAI,
        DATA_REFERENCE_ALIASES_REPOSITORY_DATA,
        DATA_REFERENCE_SERVICE_LEVEL_TRACE_INFO,
        DATA_REFERENCE_IP_ADDRESS_SECURE_BINDING_INFO,
        DATA_REFERENCE_SERVICE_PRIORITY_LEVEL,
        DATA_REFERENCE_SMS_REGISTRATION_INFO,
        DATA_REFERENCE_SERVED_USER_IDENTITY,
        DATA_REFERENCE_IMSI,
        DATA_REFERENCE_IMS_USER_STATE_EPS,
        DATA_REFERENCE_MSISDN_MAPPINGS,
        DATA_REFERENCE_STN_SR,
        DATA_REFERENCE_CSRN,
    ]

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             DataReferenceAVP.code,
                             DataReferenceAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        EnumeratedType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)


class ServiceIndicationAVP(DiameterAVP, OctetStringType):
    """Implementation of Service-Indication AVP in Section 6.3.5 of
    ETSI TS 129 329 V15.1.0 (2018-07).

    The Service-Indication AVP (AVP Code 704) is of type OctetString.
    """
    code = SH_SERVICE_INDICATION_AVP_CODE
    vendor_id = VENDOR_ID_3GPP

    def __init__(self, data):
        DiameterAVP.__init__(self,
                             ServiceIndicationAVP.code,
                             ServiceIndicationAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        DiameterAVP.set_vendor_id_bit(self, True)
        OctetStringType.__init__(self, data=data, vendor_id=VENDOR_ID_3GPP)
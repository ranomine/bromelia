# -*- coding: utf-8 -*-
"""
    bromelia.avps.ietf.rfc4590
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains Diameter AVP classes defined in IETF RFC 4590.

    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ...base import DiameterAVP
from ...constants.ietf.rfc4590 import *
from ...types import *


class DigestRealmAVP(DiameterAVP, UTF8StringType):
    """Implementation of Digest-Realm AVP in both Section 3.2 of IETF RFC 4590.

    The Digest-Realm AVP (AVP Code 104) is of type UTF8String.
    """
    code = DIGEST_REALM_AVP_CODE
    vendor_id = None

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             DigestRealmAVP.code,
                             DigestRealmAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        UTF8StringType.__init__(self, data=data)



class DigestQoPAVP(DiameterAVP, UTF8StringType):
    """Implementation of Digest-Realm AVP in both Section 3.8 of IETF RFC 4590.

    The Digest-QoP AVP (AVP Code 110) is of type UTF8String.
    """
    code = DIGEST_QOP_AVP_CODE
    vendor_id = None

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             DigestQoPAVP.code,
                             DigestQoPAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        UTF8StringType.__init__(self, data=data)
        
        
class DigestAlgorithmAVP(DiameterAVP, UTF8StringType):
    """Implementation of Digest-Realm AVP in both Section 3.9 of IETF RFC 4590.

    The Digest-Algorithm AVP (AVP Code 111) is of type UTF8String.
    """
    code = DIGEST_ALGORITHM_AVP_CODE
    vendor_id = None

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             DigestAlgorithmAVP.code,
                             DigestAlgorithmAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        UTF8StringType.__init__(self, data=data)


class DigestHA1AVP(DiameterAVP, UTF8StringType):
    """Implementation of Digest-Realm AVP in both Section 3.19 of IETF RFC 4590.

    The Digest-HA1 AVP (AVP Code 121) is of type UTF8String.
    """
    code = DIGEST_HA1_AVP_CODE
    vendor_id = None

    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             DigestHA1AVP.code,
                             DigestHA1AVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, True)
        UTF8StringType.__init__(self, data=data)        
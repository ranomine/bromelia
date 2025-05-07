# -*- coding: utf-8 -*-
"""
    bromelia.constants.ietf.rfc4590
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
    This module contains constants defined in IETF RFC 4590.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ..._internal_utils import convert_to_4_bytes


#: Diameter AVPs
DIGEST_REALM_AVP_CODE = convert_to_4_bytes(104)
DIGEST_QOP_AVP_CODE = convert_to_4_bytes(110)
DIGEST_ALGORITHM_AVP_CODE = convert_to_4_bytes(111)
DIGEST_HA1_AVP_CODE = convert_to_4_bytes(121)

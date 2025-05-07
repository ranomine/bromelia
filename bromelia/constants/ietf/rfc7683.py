# -*- coding: utf-8 -*-
"""
    bromelia.constants.ietf.rfc7683
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
    This module contains constants defined in IETF RFC 7683.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ..._internal_utils import convert_to_4_bytes


#: Diameter AVPs
OC_SUPPORTED_FEATURES_AVP_CODE = convert_to_4_bytes(621)
OC_OLR_AVP_CODE = convert_to_4_bytes(623)

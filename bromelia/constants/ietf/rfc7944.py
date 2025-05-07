# -*- coding: utf-8 -*-
"""
    bromelia.constants.ietf.rfc7944
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
    This module contains constants defined in IETF RFC 7944.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ..._internal_utils import convert_to_4_bytes


#: Diameter AVPs
DRMP_AVP_CODE = convert_to_4_bytes(301)

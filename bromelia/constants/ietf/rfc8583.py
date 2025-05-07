# -*- coding: utf-8 -*-
"""
    bromelia.constants.ietf.rfc8583
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
    This module contains constants defined in IETF RFC 8583.
    
    :copyright: (c) 2025-present Roch-Alexandre Nomine.
    :license: MIT, see LICENSE for more details.
"""

from ..._internal_utils import convert_to_4_bytes


#: Diameter AVPs
LOAD_AVP_CODE = convert_to_4_bytes(650)
LOAD_TYPE_AVP_CODE = convert_to_4_bytes(651)
LOAD_VALUE_AVP_CODE = convert_to_4_bytes(652)
SOURCEID_AVP_CODE = convert_to_4_bytes(653)
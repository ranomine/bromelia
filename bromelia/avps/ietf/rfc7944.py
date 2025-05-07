# -*- coding: utf-8 -*-
"""
    bromelia.avps.ietf.rfc7944
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains Diameter AVP classes defined in IETF RFC 7944.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ...base import DiameterAVP
from ...constants.ietf.rfc7944 import *
from ...types import *


class DRMPAVP(DiameterAVP, EnumeratedType):
    """Implementation of DRMP AVP in Section 9 of 
    IETF RFC 7944.

    The DRMP AVP (AVP Code 301) is of type Enumerated.
    """
    code = DRMP_AVP_CODE
    vendor_id = None

    values = [
                DRMP_PRIORITY_0,
                DRMP_PRIORITY_1,
                DRMP_PRIORITY_2,
                DRMP_PRIORITY_3,
                DRMP_PRIORITY_4,
                DRMP_PRIORITY_5,
                DRMP_PRIORITY_6,
                DRMP_PRIORITY_7,
                DRMP_PRIORITY_8,
                DRMP_PRIORITY_9,
                DRMP_PRIORITY_10,
                DRMP_PRIORITY_11,
                DRMP_PRIORITY_12,
                DRMP_PRIORITY_13,
                DRMP_PRIORITY_14,
                DRMP_PRIORITY_15         
    ]
    def __init__(self, data):
        DiameterAVP.__init__(self, 
                             DRMPAVP.code,
                             DRMPAVP.vendor_id)
        DiameterAVP.set_mandatory_bit(self, False)
        EnumeratedType.__init__(self, data=data)

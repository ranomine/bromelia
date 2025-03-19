# -*- coding: utf-8 -*-
"""
    bromelia.lib.etsi_3gpp_cx
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    A Python package with APIs for handling 3GPP Cx Application Id in the
    bromelia Python Library context.

    :copyright: (c) 2020-present Roch-Alexandre Nomine.
    :license: MIT, see LICENSE for more details.
"""

from .avps import *

from .messages import UserAuthorizationAnswer as UAA
from .messages import UserAuthorizationRequest as UAR

from .messages import ServerAssignmentAnswer as SAA
from .messages import ServerAssignmentRequest as SAR

from .messages import LocationInfoAnswer as LIA
from .messages import LocationInfoRequest as LIR

from .messages import MultimediaAuthAnswer as MAA
from .messages import MultimediaAuthRequest as MAR

from .messages import RegistrationTerminationAnswer as RTA
from .messages import RegistrationTerminationRequest as RTR

from .messages import PushProfileAnswer as PPA
from .messages import PushProfileRequest as PPR

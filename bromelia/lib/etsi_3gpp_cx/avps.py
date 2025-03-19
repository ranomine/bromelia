# -*- coding: utf-8 -*-
"""
    bromelia.lib.etsi_3gpp_cx.avps
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the Diameter protocol AVP library that are used 
    to create Diameter messages for 3GPP Cx Application Id.
    
    :copyright: (c) 2020-present Roch-Alexandre Nomine
    :license: MIT, see LICENSE for more details.
"""

from ...avps.etsi_3gpp.ts_129_212 import RatTypeAVP

from ...avps.etsi_3gpp.ts_129_229 import SupportedFeaturesAVP
from ...avps.etsi_3gpp.ts_129_229 import VisitedNetworkIdentifierAVP
from ...avps.etsi_3gpp.ts_129_229 import ServerAssignmentTypeAVP
from ...avps.etsi_3gpp.ts_129_229 import ServerCapabilitiesTypeAVP

from ...avps.ietf.rfc6733 import AuthApplicationIdAVP
from ...avps.ietf.rfc6733 import AuthSessionStateAVP
from ...avps.ietf.rfc6733 import DestinationHostAVP
from ...avps.ietf.rfc6733 import DestinationRealmAVP
from ...avps.ietf.rfc6733 import ExperimentalResultAVP
from ...avps.ietf.rfc6733 import FailedAvpAVP
from ...avps.ietf.rfc6733 import OriginHostAVP
from ...avps.ietf.rfc6733 import OriginRealmAVP
from ...avps.ietf.rfc6733 import ProxyInfoAVP
from ...avps.ietf.rfc6733 import ResultCodeAVP
from ...avps.ietf.rfc6733 import RouteRecordAVP
from ...avps.ietf.rfc6733 import SessionIdAVP
from ...avps.ietf.rfc6733 import UserNameAVP
from ...avps.ietf.rfc6733 import VendorIdAVP
from ...avps.ietf.rfc6733 import VendorSpecificApplicationIdAVP

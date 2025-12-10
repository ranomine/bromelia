# -*- coding: utf-8 -*-
"""
    bromelia.lib.etsi_3gpp_s6a.avps
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains the Diameter protocol AVP library that are used 
    to create Diameter messages for 3GPP S6a/S6d Application Id.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

from ...avps.ietf.rfc6733 import SessionIdAVP
from ...avps.ietf.rfc6733 import VendorSpecificApplicationIdAVP
from ...avps.ietf.rfc6733 import AuthSessionStateAVP
from ...avps.ietf.rfc6733 import OriginHostAVP
from ...avps.ietf.rfc6733 import OriginRealmAVP
from ...avps.ietf.rfc6733 import DestinationHostAVP
from ...avps.ietf.rfc6733 import DestinationRealmAVP
from ...avps.ietf.rfc6733 import UserNameAVP
from ...avps.ietf.rfc6733 import RouteRecordAVP

from ...avps.etsi_3gpp.ts_129_229 import SupportedFeaturesAVP
from ...avps.etsi_3gpp.ts_129_229 import PublicIdentityAVP
from ...avps.etsi_3gpp.ts_129_229 import VisitedNetworkIdentifierAVP
from ...avps.etsi_3gpp.ts_129_229 import UserAuthorizationTypeAVP
from ...avps.etsi_3gpp.ts_129_229 import UARFlagsAVP
from ...avps.etsi_3gpp.ts_129_229 import ServerNameAVP
from ...avps.etsi_3gpp.ts_129_229 import ServerCapabilitiesAVP
from ...avps.etsi_3gpp.ts_129_229 import UserDataAVP
from ...avps.etsi_3gpp.ts_129_229 import OriginatingRequestAVP
from ...avps.etsi_3gpp.ts_129_229 import ChargingInformationAVP
from ...avps.etsi_3gpp.ts_129_229 import AssociatedIdentitiesAVP
from ...avps.etsi_3gpp.ts_129_229 import LooseRouteInformationAVP
from ...avps.etsi_3gpp.ts_129_229 import PCSCFSubscriptionInfoAVP
from ...avps.etsi_3gpp.ts_129_229 import SCSCFRestorationInfoAVP
from ...avps.etsi_3gpp.ts_129_229 import AssociatedRegisteredIdentitiesAVP
from ...avps.etsi_3gpp.ts_129_229 import WildcardedPublicIdentityAVP
from ...avps.etsi_3gpp.ts_129_229 import ServerAssignmentTypeAVP
from ...avps.etsi_3gpp.ts_129_229 import UserDataAVP
from ...avps.etsi_3gpp.ts_129_229 import PriviledgedSenderIndicationAVP
from ...avps.etsi_3gpp.ts_129_229 import UserDataAlreadyAvailableAVP
from ...avps.etsi_3gpp.ts_129_229 import MultipleRegistrationIndicationAVP
from ...avps.etsi_3gpp.ts_129_229 import AllowedWAFWWSFIdentitiesAVP
from ...avps.etsi_3gpp.ts_129_229 import SARFlagsAVP
from ...avps.etsi_3gpp.ts_129_229 import SessionPriorityAVP
from ...avps.etsi_3gpp.ts_129_229 import SIPNumberAuthItemsAVP
from ...avps.etsi_3gpp.ts_129_229 import SIPAuthDataItemAVP
from ...avps.etsi_3gpp.ts_129_229 import LIAFlagsAVP
from ...avps.etsi_3gpp.ts_129_229 import RTRFlagsAVP
from ...avps.etsi_3gpp.ts_129_229 import DeregistrationReasonAVP
from ...avps.etsi_3gpp.ts_129_229 import IdentityWithEmergencyRegistrationAVP
from ...avps.ietf.rfc6733 import AuthApplicationIdAVP
from ...avps.ietf.rfc6733 import ExperimentalResultAVP
from ...avps.ietf.rfc6733 import FailedAvpAVP
from ...avps.ietf.rfc6733 import ProxyInfoAVP
from ...avps.ietf.rfc6733 import ResultCodeAVP

from ...avps.ietf.rfc4590 import DigestAlgorithmAVP
from ...avps.ietf.rfc4590 import DigestHA1AVP
from ...avps.ietf.rfc4590 import DigestQoPAVP
from ...avps.ietf.rfc4590 import DigestRealmAVP


from ...avps.ietf.rfc6733 import VendorIdAVP

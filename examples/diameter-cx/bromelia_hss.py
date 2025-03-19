# -*- coding: utf-8 -*-
"""
    examples.bromelia_hss
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains an example on how to setup a dummy HSS
	by using the Bromelia class features of bromelia library.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

import os
import sys

basedir = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.dirname(basedir)
bromelia_dir = os.path.dirname(examples_dir)

sys.path.insert(0, bromelia_dir)

from bromelia import Bromelia
from bromelia.avps import *
from bromelia.constants import *
from bromelia.lib.etsi_3gpp_cx import *
from bromelia.lib.etsi_3gpp_cx import UAR # UserAuthorizationRequest
from bromelia.lib.etsi_3gpp_cx import UAA # UserAuthorizationAnswer

#: Application initialization 
config_file = os.path.join(basedir, "bromelia_hss_config.yaml")

app = Bromelia(config_file=config_file)
app.load_messages_into_application_id([UAA, UAR], DIAMETER_APPLICATION_Cx)

@app.route(application_id=DIAMETER_APPLICATION_Cx, command_code=USER_AUTHORIZATION_MESSAGE)
def uar(request):
    return UAA(result_code=DIAMETER_SUCCESS)

if __name__ == "__main__":
    app.run()   #: It will be blocked until connection has been established

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    examples.cx-proxy
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains an example on how to setup a dummy HSS
	by using the Bromelia class features of bromelia library.
    
    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

import os
import sys
import uuid

basedir = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.dirname(basedir)
bromelia_dir = os.path.dirname(examples_dir)

sys.path.insert(0, bromelia_dir)


from bromelia import Bromelia
from bromelia.avps.ietf.rfc6733 import DestinationRealmAVP, ProxyInfoAVP, ProxyHostAVP, ProxyStateAVP
from bromelia.constants.app_ids import DIAMETER_APPLICATION_Cx
from bromelia.lib.etsi_3gpp_cx import UAA

def handle_request(request):
    print(f"Received request with Hop-by-Hop ID: {request.header.hop_by_hop_identifier}")
    print(f"Destination-Realm: {request.get_avp(DestinationRealmAVP)}")

    # Clone the request to modify and forward it
    forwarded_request = request.copy()

    # Change the destination realm
    forwarded_request.update_avp(DestinationRealmAVP("new.realm.example"))

    # Add Proxy-Info to help track forwarding
    forwarded_request.add_avp(ProxyInfoAVP(
        ProxyHostAVP("proxy.local"),
        ProxyStateAVP("state-token-001")
    ))

    # Generate a new Hop-by-Hop ID (End-to-End ID must stay the same)
    forwarded_request.header.hop_by_hop_identifier = int.from_bytes(uuid.uuid4().bytes[:4], byteorder='big')

    print(f"Forwarding with new Hop-by-Hop ID: {forwarded_request.header.hop_by_hop_identifier}")

    # Send the modified request using the same connection it came from
    request.connection.send(forwarded_request.encode())

def main():
    # Initialize Bromelia
    app = Bromelia(config_file="./config/diameter.conf")

    # Register the request handler
    app.route(DIAMETER_APPLICATION_Cx, handle_request)

    # Run the application
    app.run()

if __name__ == "__main__":
    main()

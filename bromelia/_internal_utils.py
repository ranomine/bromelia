# -*- coding: utf-8 -*-
"""
    bromelia._internal_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Defines utility functions that are consumed internally by the library.

    :copyright: (c) 2020-present Henrique Marques Ribeiro.
    :license: MIT, see LICENSE for more details.
"""

import datetime
import ipaddress
import logging
import re
import os
import struct
import yaml
from collections import namedtuple

from .definitions import diameter_application_ids
from .definitions import diameter_avps
from .definitions import diameter_command_codes
from .exceptions import InvalidConfigKey
from .exceptions import InvalidConfigValue


LocalNode = namedtuple("LocalNode", [
                                        "host_name",
                                        "realm",
                                        "ip_address",
                                        "port"
                                    ]
)
PeerNode = namedtuple("PeerNode", [
                                        "host_name",
                                        "realm",
                                        "ip_address",
                                        "port"
                                    ]
)
Connection = namedtuple("Connection", [
                                        "name",
                                        "mode",
                                        "transport_type",
                                        "local_node",
                                        "peer_node",
                                        "application_ids",
                                        "watchdog_timeout",
                                        "accepted_realms"
                                    ]
)
config_mask = [
                "MODE",
                "TRANSPORT_TYPE",
                "APPLICATIONS",
                "LOCAL_NODE_HOSTNAME",
                "LOCAL_NODE_REALM",
                "LOCAL_NODE_IP_ADDRESS",
                "LOCAL_NODE_PORT",
                "PEER_NODE_HOSTNAME",
                "PEER_NODE_REALM",
                "PEER_NODE_IP_ADDRESS",
                "PEER_NODE_PORT",
                "WATCHDOG_TIMEOUT"
]


def convert_to_1_byte(content: int) -> bytes:
    return struct.pack(">B", content)


def convert_to_2_bytes(content: int) -> bytes:
    return struct.pack(">H", content)


def convert_to_3_bytes(content: int) -> bytes:
    return content.to_bytes(3, byteorder="big")


def convert_to_4_bytes(content: int) -> bytes:
    return struct.pack(">L", content)


def convert_to_6_bytes(content: int) -> bytes:
    return content.to_bytes(6, byteorder="big")


def convert_to_8_bytes(content: int) -> bytes:
    return struct.pack(">q", content)


def convert_to_integer_from_bytes(bytes: bytes) -> int:
    return int.from_bytes(bytes, byteorder="big")


def header_representation(header) -> dict:
    cmd_code = header.command_code
    application_id = header.application_id
    
    cmd_code_str, cmd_code_int = command_code_look_up(cmd_code)

    flag_representation = ""
    if header.is_request():
        flag_representation += " REQ|"
        cmd_code_str = cmd_code_str[:3]
    else:
        flag_representation += " "
        cmd_code_str = cmd_code_str[4:]

    if header.is_proxiable():
        flag_representation += "PXY|"

    if header.is_error():
        flag_representation += "ERR|"

    application_id = header.application_id
    app_id_str, app_id_int = application_id_look_up(application_id)

    return {
                "cmd_code_str": cmd_code_str,
                "cmd_code_int": cmd_code_int,
                "flag_representation": flag_representation[:-1],
                "app_id_str": app_id_str,
                "app_id_int": app_id_int
    }


def application_id_look_up(application_id: bytes) -> tuple[str, str]:
    if not application_id:
        return "", "Unknown"
    
    for application in diameter_application_ids:
        if application["id"] == convert_to_integer_from_bytes(application_id):
            return application["long_name"], application["id"]
    return "", "Unknown"


def command_code_look_up(command_code: bytes) -> tuple[str, str]:
    if not command_code:
        return "", "Unknown"

    for code in diameter_command_codes:
        if code["id"] == convert_to_integer_from_bytes(command_code):
            return code["short_name"], code["id"]
    return "", "Unknown"


def avp_look_up(avp) -> str:
    if not avp.get_vendor_id():
        if avp.get_code() == 0:
            return "Unknown"

        for diameter_avp in diameter_avps:
            if diameter_avp["id"] == avp.get_code():
                return diameter_avp["name"]

    return "Unknown"



def _convert_config_to_connection_obj(config) -> Connection:
    """Convert a config dict to a Connection object."""
    connection = Connection()

    connection.local_node = LocalNode(
        host_name=config["LOCAL_NODE_HOSTNAME"],
        realm=config["LOCAL_NODE_REALM"],
        ip_address=config["LOCAL_NODE_IP_ADDRESS"],
        port=config["LOCAL_NODE_PORT"]
    )

    connection.peer_node = PeerNode(
        host_name=config["PEER_NODE_HOSTNAME"],
        realm=config["PEER_NODE_REALM"],
        ip_address=config["PEER_NODE_IP_ADDRESS"],
        port=config["PEER_NODE_PORT"]
    )

    connection.application_ids = config["APPLICATIONS"]
    connection.accepted_realms = config.get("accepted_realms", [config["LOCAL_NODE_REALM"]])
    connection.watchdog_timeout = config["WATCHDOG_TIMEOUT"]
    connection.transport_type = config["TRANSPORT_TYPE"]

    return connection


def _convert_file_to_config(filepath: str = None, variables_dictionary: dict = globals()) -> list:
    if not filepath:
        filepath = os.path.join(os.getcwd(), "config.yaml")

    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as config_file:
                from_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

    except Exception as e:
        logging.exception(f"_convert_file_to_config - exception: {e}")

    if from_config_file["api_version"] != "v1":
        raise

    configs = list()
    transport_type = "tcp"

    for spec in from_config_file["spec"]:
        for application in spec["applications"]:
            vendor_id = application["vendor_id"]
            app_id = application["app_id"]

            application["vendor_id"] = variables_dictionary[vendor_id]
            application["app_id"] = variables_dictionary[app_id]

        if spec.get("transport_type"):
            transport_type = spec["transport_type"]

        configs.append({
                            "MODE": spec["mode"].upper(),
                            "TRANSPORT_TYPE": transport_type.upper(),
                            "APPLICATIONS": spec["applications"],
                            "LOCAL_NODE_HOSTNAME": spec["local"]["hostname"],
                            "LOCAL_NODE_REALM": spec["local"]["realm"],
                            "LOCAL_NODE_IP_ADDRESS": spec["local"]["ip_address"],
                            "LOCAL_NODE_PORT": spec["local"]["port"],
                            "PEER_NODE_HOSTNAME": spec["peer"]["hostname"],
                            "PEER_NODE_REALM": spec["peer"]["realm"],
                            "PEER_NODE_IP_ADDRESS": spec["peer"]["ip_address"],
                            "PEER_NODE_PORT": spec["peer"]["port"],
                            "WATCHDOG_TIMEOUT": spec["watchdog_timeout"]
        })

    return configs


def get_app_ids(apps: list) -> str:
    text = ""
    for index, app in enumerate(apps):
        app_name = application_id_look_up(app['app_id'])[0]
        text += f"{app_name};"
        if index == (len(apps) - 1):
            return text[:-1]


def get_app_name(filepath: str = None) -> str:
    if not filepath:
        filepath = os.path.join(os.getcwd(), "config.yaml")

    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as config_file:
                from_config_file = yaml.load(config_file, Loader=yaml.FullLoader)

    except Exception as e:
        logging.exception(f"_convert_file_to_config - exception: {e}")

    if from_config_file["api_version"] != "v1":
        raise

    return from_config_file["name"]


def get_logging_filename(app_name: str = None) -> str:
    if app_name is None:
        name = "dsa"
    else:
        if not isinstance(app_name, str) or app_name == "":
            name = "dsa"
        else:
            pattern = re.findall(r"[\-\+\*\/\\\!\@\#\$\%\&\\(\)\=\~\[\]\{\}]", app_name)
            if pattern:
                raise Exception("Invalid symbol found")

            name = app_name.lower()

    now = datetime.datetime.now()

    #: The filename has the follow format:
    #: log-{name}-{year}-{month}-{day}-{hour}-{minute}-{second}-UTC{utc}-pid_{pid}.log
    return f"log-{name}-"\
           f"{str(now.year).zfill(2)}-"\
           f"{str(now.month).zfill(2)}-"\
           f"{str(now.day).zfill(2)}-"\
           f"{str(now.hour).zfill(2)}-"\
           f"{str(now.minute).zfill(2)}-"\
           f"{str(now.second).zfill(2)}-"\
           f"UTC{str(now.astimezone())[-6:-3]}-"\
           f"pid_{os.getpid()}.log"


def get_avp_name_formatted(key: str) -> str:
    pattern = re.findall(r"(.*)__(\d*)", key)
    if pattern:
        key = pattern[0][0]
        idx = pattern[0][1]
        return f"{key}_avp__{idx}"

    return f"{key}_avp"


class SessionHandler:
    init = 0
    id = 0
    optional = "bromelia"


    def __init__(self):
        SessionHandler.reset()


    @staticmethod
    def get_session_id(data: str, previous: str = None) -> str:
        #: Returns high, low and optional values in order to fulfill the 
        #: recommended format: 
        #: <DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]

        SessionHandler._verify_session_id(previous, current=data)

        high = SessionHandler.init
        low = SessionHandler.id
        optional = SessionHandler.optional

        return f"{data};{high};{low};{optional}"


    @staticmethod
    def reset() -> None:
        diff = datetime.datetime.utcnow() - datetime.datetime(1900, 1, 1, 0, 0, 0)
        SessionHandler.init = diff.days*24*60*60 + diff.seconds
        SessionHandler.id = 0


    @staticmethod
    def _verify_session_id(previous: str, current: str) -> None:
        if previous is not None:
            _previous = previous.split(";")

            if _previous:
                if current == _previous[0]:
                    SessionHandler.id += 1
                    return

            SessionHandler.reset()
            return
        
        SessionHandler.id += 1


SessionHandler()
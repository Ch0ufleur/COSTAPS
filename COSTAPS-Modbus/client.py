#!/usr/bin/env python3
"""Pymodbus Synchronous Client Example.

An example of a single threaded synchronous client.

usage::

    client_sync.py [-h] [-c {tcp,udp,serial,tls}]
                    [-f {ascii,binary,rtu,socket,tls}]
                    [-l {critical,error,warning,info,debug}] [-p PORT]
                    [--baudrate BAUDRATE] [--host HOST]

    -h, --help
        show this help message and exit
    -c, --comm {tcp,udp,serial,tls}
        set communication, default is tcp
    -f, --framer {ascii,binary,rtu,socket,tls}
        set framer, default depends on --comm
    -l, --log {critical,error,warning,info,debug}
        set log level, default is info
    -p, --port PORT
        set port
    --baudrate BAUDRATE
        set serial device baud rate
    --host HOST
        set host, default is 127.0.0.1

The corresponding server must be started before e.g. as:

    python3 server_sync.py

"""
import argparse
import logging
import time

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.client import (
    ModbusTcpClient,
    ModbusTlsClient
)

# from .helper import get_certificate, get_commandline


logging.basicConfig()
_logger = logging.getLogger(__file__)
_logger.setLevel("DEBUG")


def setup_sync_client(description=None):
    """Run client setup."""
    _logger.info("### Create client object")
    if "tcp" == "tcp":
        client = ModbusTcpClient(
            host="127.0.0.1",
            port="1502",
            # Common optional parameters:
            # framer=args.framer,
            # timeout=args.timeout,
            #    retries=3,
            #    retry_on_empty=False,y
            #    close_comm_on_error=False,
            #    strict=True,
            # TCP setup parameters
            #    source_address=("localhost", 0),
        )
    # elif args.comm == "tls":  # pragma no cover
    #     client = ModbusTlsClient(
    #         args.host,
    #         port=args.port,
    #         # Common optional parameters:
    #         framer=args.framer,
    #         timeout=args.timeout,
    #         #    retries=3,
    #         #    retry_on_empty=False,
    #         #    close_comm_on_error=False,
    #         #    strict=True,
    #         # TLS setup parameters
    #         #    sslctx=None,
    #         certfile=get_certificate("crt"),
    #         keyfile=get_certificate("key"),
    #         #    password=None,
    #         server_hostname="localhost",
    #     )
    return client

def run_a_few_calls(client: ModbusTcpClient):
    """Test connection works."""
    # rr = client.read_coils(32, 1, slave=1)
    rr = client.read_holding_registers(0, 1, slave=1)
    print(rr.registers)

    rr = client.write_register(0, 3, slave=1)
    print(rr)

    rr = client.write_registers(0, [1, 1, 3, 3, 2, 2], slave=1)
    print(rr)

    rr = client.read_holding_registers(3, 1, slave=1)
    print(rr.registers)

    # assert len(rr.bits) == 8
    rr = client.read_holding_registers(0, 6, slave=1)
    print(rr.registers)
    # assert rr.registers[0] == 17

def logic_sim1(client: ModbusTcpClient):
    class TrafficLightStates:
        INITIALIZING = 1
        NORTBOUND_GREEN = 2
        MIDDLE_RED = 3
        SOUTHBOUND_GREEN = 4

    # class TrafficLightValues:
        
    first_trafficlight_id = 0
    second_trafficlight_id = 1
    third_trafficlight_id = 2
    fourth_trafficlight_id = 3
    fifth_trafficlight_id = 4

    currentStatus = TrafficLightStates.INITIALIZING
    pastStatus = None

    while(True):
        if(currentStatus == TrafficLightStates.INITIALIZING):
            _logger.info("### Initializing")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(third_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTBOUND_GREEN
            pastStatus = TrafficLightStates.INITIALIZING

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.NORTBOUND_GREEN):
            _logger.info("### Northbound green")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(third_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.MIDDLE_RED
            pastStatus = TrafficLightStates.NORTBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.MIDDLE_RED):
            _logger.info("### Middle red")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(third_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)

            if pastStatus == TrafficLightStates.SOUTHBOUND_GREEN:
                currentStatus = TrafficLightStates.NORTBOUND_GREEN
            else:
                currentStatus = TrafficLightStates.SOUTHBOUND_GREEN
            pastStatus = TrafficLightStates.MIDDLE_RED

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.SOUTHBOUND_GREEN):
            _logger.info("### Southbound green")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(third_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.MIDDLE_RED
            pastStatus = TrafficLightStates.SOUTHBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)


#"""Combine setup and run."""
testclient = setup_sync_client()
# run_sync_client(testclient, modbus_calls=run_a_few_calls)

#"""Run sync client."""
_logger.info("### Client starting")
testclient.connect()
# if run_a_few_calls:
#     run_a_few_calls(testclient)

logic_sim1(testclient)

testclient.close()
_logger.info("### End of Program")

#!/usr/bin/env python3
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

logging.basicConfig()
_logger = logging.getLogger(__file__)
_logger.setLevel("DEBUG")


def setup_sync_client(args):
    """Run client setup."""
    _logger.info("### Create client object")
    if args.comm == "tcp":
        client = ModbusTcpClient(
            host=args.host,
            port=args.port,
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
    # elif args.comm == "tls":
    #     client = ModbusTlsClient(
    #         args.host,
    #         port=args.port,
    #         # Common optional parameters:
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

def run_a_few_test_calls(client: ModbusTcpClient):
    """Test connection works."""
    # rr = client.read_coils(32, 1, slave=1)
    rr = client.read_holding_registers(0, 1, slave=1)
    print(rr.registers)

    rr = client.write_register(0, 3, slave=1)
    print(rr.isError())

    rr = client.write_registers(0, [1, 1, 3, 3, 2, 2], slave=1)
    print(rr)
    # print(rr.)

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

    first_trafficlight_id = 0 * 6
    second_trafficlight_id = 1 * 6
    third_trafficlight_id = 2 * 6
    fourth_trafficlight_id = 3 * 6
    fifth_trafficlight_id = 4 * 6

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
            # pastStatus = TrafficLightStates.MIDDLE_RED

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

def logic_sim2(client: ModbusTcpClient):
    class TrafficLightStates:
        INITIALIZING = 1
        NORTH_SOUTH_GREEN = 2
        NORTH_SOUTH_YELLOW = 3
        ALL_RED = 4
        EAST_WEST_GREEN = 5
        EAST_WEST_YELLOW = 6

    # class TrafficLightValues:
        
    first_trafficlight_id = 0 * 6
    second_trafficlight_id = 1 * 6

    currentStatus = TrafficLightStates.INITIALIZING
    pastStatus = None

    while(True):
        if(currentStatus == TrafficLightStates.INITIALIZING):
            _logger.info("### Initializing")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTH_SOUTH_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.NORTH_SOUTH_GREEN):
            _logger.info("### North-South green")
            rr = client.write_registers(first_trafficlight_id, [1, 0, 0, 1, 0, 0], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTH_SOUTH_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.NORTH_SOUTH_YELLOW):
            _logger.info("### North-South yellow")
            rr = client.write_registers(first_trafficlight_id, [0, 1, 0, 0, 1, 0], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.ALL_RED
            pastStatus = TrafficLightStates.NORTH_SOUTH_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.ALL_RED):
            _logger.info("### All red")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)

            # currentStatus = TrafficLightStates.EAST_WEST_GREEN

            if pastStatus == TrafficLightStates.EAST_WEST_YELLOW:
                currentStatus = TrafficLightStates.NORTH_SOUTH_GREEN
            else:
                currentStatus = TrafficLightStates.EAST_WEST_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.EAST_WEST_GREEN):
            _logger.info("### East-West green")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [1, 0, 0, 1, 0, 0], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.EAST_WEST_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.EAST_WEST_YELLOW):
            _logger.info("### East-West yellow")
            rr = client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = client.write_registers(second_trafficlight_id, [0, 1, 0, 0, 1, 0], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.ALL_RED
            pastStatus = TrafficLightStates.EAST_WEST_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)

parser = argparse.ArgumentParser(prog='Client Modbus')
parser.add_argument('--host', default="127.0.0.1")
parser.add_argument('--port', default="502")
parser.add_argument('--sim', choices=['sim1', 'sim2'], required=True)
parser.add_argument('--comm', choices=['tcp', 'tsl'], required=True)
args = parser.parse_args()
# print(args.host, args.port, args.sim, args.comm)

#"""Combine setup and run."""
testclient = setup_sync_client(args)
#"""Run sync client."""
_logger.info("### Client starting")
testclient.connect()
# run_a_few_test_calls(testclient)
if args.sim == "sim1":
    logic_sim1(testclient)
elif args.sim == "sim2":
    logic_sim2(testclient)
testclient.close()
_logger.info("### End of Program")
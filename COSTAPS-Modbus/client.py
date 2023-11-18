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

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from pymodbus.client import (
    ModbusSerialClient,
    ModbusTcpClient,
    ModbusTlsClient,
    ModbusUdpClient,
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
            port="502",
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


def run_sync_client(client, modbus_calls=None):
    """Run sync client."""
    _logger.info("### Client starting")
    client.connect()
    if modbus_calls:
        modbus_calls(client)
    client.close()
    _logger.info("### End of Program")


def run_a_few_calls(client: ModbusTcpClient):
    """Test connection works."""
    # rr = client.read_coils(32, 1, slave=1)
    rr = client.read_holding_registers(0, 1, slave=1)
    print(rr.registers)

    #rr = client.write_register(0, 3, slave=1)
    rr = client.write_registers(0, [1,0,0,0,0,1], slave=1)
    print(rr)

    # assert len(rr.bits) == 8
    rr = client.read_holding_registers(0, 1, slave=1)
    print(rr.registers)
    # assert rr.registers[0] == 17
    # assert rr.registers[1] == 17


"""Combine setup and run."""
testclient = setup_sync_client(
    description="Run synchronous client."
)
run_sync_client(testclient, modbus_calls=run_a_few_calls)

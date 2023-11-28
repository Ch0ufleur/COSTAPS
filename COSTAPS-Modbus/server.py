#!/usr/bin/env python3
"""Pymodbus asynchronous Server Example.

An example of a multi threaded asynchronous server.

usage::

    server_async.py [-h] [--comm {tcp,udp,serial,tls}]
                    [--framer {ascii,binary,rtu,socket,tls}]
                    [--log {critical,error,warning,info,debug}]
                    [--port PORT] [--store {sequential,sparse,factory,none}]
                    [--slaves SLAVES]

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
        set serial device baud rate
    --store {sequential,sparse,factory,none}
        set datastore type
    --slaves SLAVES
        set number of slaves to respond to

The corresponding client can be started as:

    python3 client_sync.py

"""
import asyncio
import logging
import helper
import socket
import json

from pymodbus import __version__ as pymodbus_version
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import (
    StartAsyncTcpServer,
    StartAsyncTlsServer,
)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__file__)
_logger.setLevel(logging.DEBUG)

# Default
simhost = "127.0.0.1"
simport = 12345

def send_tcp_request(address, values):
    #communication server address and port
    server_address = (simhost, simport)

    # print(f"##### Sending packet to: {server_address[0]}:{server_address[1]}")
    # return

    plc_json = {
        "id": address ,
        "states": [
            ## Northbound - East
            {
                "green": int(values[0]),
                "yellow": int(values[1]),
                "red": int(values[2])
            },
            ## Southbound - West
            {
                "green": int(values[3]),
                "yellow": int(values[4]),
                "red": int(values[5])
            }
        ]
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)

        # Convert JSON input to a string and send it to the server
        plc_json_str = json.dumps(plc_json)
        client_socket.sendall(plc_json_str.encode())
        print(f"Sent JSON request to server: {plc_json_str}")
        client_socket.close()
        # Receive the response from the server
        # response_json = client_socket.recv(1024).decode()
        # print(f"Received response from server: {response_json}")


class CustomDataBlock(ModbusSequentialDataBlock):

    def getValues(self, address, count=1):
        # _logger.info("Address read: " + str(address))
        return super().getValues(address, count)


    def setValues(self, address, values):
        _logger.info("Address written: " + str(address % 5))
        _logger.info("Values changed: " + str(values))
        # send tcp request to Unity Sim
        send_tcp_request(address % 5, values)
        return super().setValues(address, values)


def setup_server(description=None, cmdline=None):
    """Run server setup."""
    args = helper.get_commandline(server=True, description=description, cmdline=cmdline)
    _logger.info("### Create datastore")

    datablock = CustomDataBlock(0x00, [0] * 100)
    coil = CustomDataBlock(0x00, [0] * 100)
    context = ModbusSlaveContext(
        di=datablock, co=coil, hr=datablock, ir=datablock, zero_mode=True
    )
    single = True

    # Build data storage
    args.context = ModbusServerContext(slaves=context, single=single)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    # If you don't set this or any fields, they are defaulted to empty strings.
    # ----------------------------------------------------------------------- #
    args.identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "COSTAPS",
            "ProductCode": "INF6103",
            "VendorUrl": "",
            "ProductName": "Bedtest",
            "ModelName": "Bedtest Beta",
            "MajorMinorRevision": pymodbus_version,
        }
    )

    # Set Unity simulation address
    global simhost
    simhost = args.simhost
    global simport 
    simport = args.simport

    return args


async def run_async_server(args):
    """Run server."""
    txt = f"### start ASYNC server, listening on {args.port} - {args.comm}"
    _logger.info(txt)

    if args.comm == "tcp":
        address = (args.host if args.host else "0.0.0.0", args.port if args.port else 5020)
        server = await StartAsyncTcpServer(
            context=args.context,  # Data storage
            identity=args.identity,  # server identify
            address=address,  # listen address
        )
    elif args.comm == "tls":
        address = (args.host if args.host else "0.0.0.0", args.port if args.port else 5020)
        server = await StartAsyncTlsServer(
            context=args.context,  # Data storage
            host="localhost",  # define tcp address where to connect to.
            identity=args.identity,  # server identify
            address=address,  # listen address
            certfile="./certificates/pymodbus.crt", # The cert file path for TLS (used if sslctx is None)
            keyfile="./certificates/pymodbus.key",  # The key file path for TLS (used if sslctx is None)
            password="pass",  # The password for for decrypting the private key file
        )
    return server


async def async_helper():
    """Combine setup and run."""
    _logger.info("Starting...")
    run_args = setup_server(description="Run asynchronous server.")
    await run_async_server(run_args)


if __name__ == "__main__":
    asyncio.run(async_helper(), debug=True)  # pragma: no cover
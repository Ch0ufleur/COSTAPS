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


def send_tcp_request(address, values):
    #communication server address and port
    server_address = (args.host_tcp, args.port_tcp)
    plc_json = {
        "id": address ,
        "states": [
            ## Northbound - East
            {
                "green": values[0],
                "yellow": values[1],
                "red": values[2]
            },
            ## Southbound - West
            {
                "green": values[3],
                "yellow": values[4],
                "red": values[5]
            }
        ]
    }
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)

        # Convert JSON input to a string and send it to the server
        plc_json_str = json.dumps(plc_json)
        client_socket.sendall(plc_json_str.encode())
        print(f"Sent JSON request to server: {plc_json_str}")
        client_socket.close();
        # Receive the response from the server
        # response_json = client_socket.recv(1024).decode()
        # print(f"Received response from server: {response_json}")


class CustomDataBlock(ModbusSequentialDataBlock):

    def getValues(self, address, count=1):
        _logger.info("Address read: " + str(address))
        return super().getValues(address, count)


    def setValues(self, address, values):
        _logger.info("Address written: " + str(address))
        _logger.info("Values changed: " + str(values))
        # send tcp request to Unity Sim
        # send_tcp_request(address % 5, values)
        return super().setValues(address, values)
    

def setup_server(description=None, cmdline=None):
    """Run server setup."""
    args = helper.get_commandline(server=True, description=description, cmdline=cmdline)
    _logger.info("### Create datastore")

    datablock = CustomDataBlock(0x00, [0] * 100)
    context = ModbusSlaveContext(
        di=datablock, co=datablock, hr=datablock, ir=datablock, zero_mode=True
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
            "VendorName": "Pymodbus",
            "ProductCode": "PM",
            "VendorUrl": "https://github.com/pymodbus-dev/pymodbus/",
            "ProductName": "Pymodbus Server",
            "ModelName": "Pymodbus Server",
            "MajorMinorRevision": pymodbus_version,
        }
    )
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
            # TBD host=
            # TBD port=
            address=address,  # listen address
            # custom_functions=[],  # allow custom handling
            # framer=args.framer,  # The framer strategy to use
            # ignore_missing_slaves=True,  # ignore request to a missing slave
            # broadcast_enable=False,  # treat slave_id 0 as broadcast address,
            # timeout=1,  # waiting time for request to complete
            # TBD strict=True,  # use strict timing, t1.5 for Modbus RTU
        )
    elif args.comm == "tls":
        address = (args.host if args.host else "0.0.0.0", args.port if args.port else 5020)
        server = await StartAsyncTlsServer(
            context=args.context,  # Data storage
            host="localhost",  # define tcp address where to connect to.
            # port=port,  # on which port
            identity=args.identity,  # server identify
            # custom_functions=[],  # allow custom handling
            address=address,  # listen address
            # framer=args.framer,  # The framer strategy to use
            certfile="./certificates/pymodbus.crt", # The cert file path for TLS (used if sslctx is None)
            # sslctx=sslctx,  # The SSLContext to use for TLS (default None and auto create)
            keyfile="./certificates/pymodbus.key",  # The key file path for TLS (used if sslctx is None)
            password="pass",  # The password for for decrypting the private key file
            # ignore_missing_slaves=True,  # ignore request to a missing slave
            # broadcast_enable=False,  # treat slave_id 0 as broadcast address,
            # timeout=1,  # waiting time for request to complete
            # TBD strict=True,  # use strict timing, t1.5 for Modbus RTU
        )
    return server


async def async_helper():
    """Combine setup and run."""
    _logger.info("Starting...")
    run_args = setup_server(description="Run asynchronous server.")
    await run_async_server(run_args)


if __name__ == "__main__":
    asyncio.run(async_helper(), debug=True)  # pragma: no cover
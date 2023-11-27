#!/usr/bin/env python3
import asyncio
import logging

import pymodbus.client as ModbusClient
from pymodbus import (
    pymodbus_apply_logging_config,
)

import helper
import sim_async

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)

logging.getLogger('asyncio').setLevel(logging.ERROR)

def setup_client(description=None, cmdline=None):
    args = helper.get_commandline(description=description, cmdline=None)
    _logger.info("### Create client")

    # activate debugging
    # pymodbus_apply_logging_config("DEBUG")

    print("get client")
    if args.comm == "tcp":
        client = ModbusClient.AsyncModbusTcpClient(
            args.host,
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
    elif args.comm == "tls":
        client = ModbusClient.AsyncModbusTlsClient(
            args.host,
            port=args.port,
            # Common optional parameters:
            # framer=args.framer,
            # timeout=args.timeout,
            #    retries=3,
            #    retry_on_empty=False,
            #    close_comm_on_error=False,
            #    strict=True,
            # TLS setup parameters
            #    sslctx=None,
            certfile="./certificates/pymodbus.crt",
            keyfile="./certificates/pymodbus.key",
            password="pass",
            server_hostname="localhost",
        )
    else:  # pragma no cover
        print(f"Unknown client {args.comm} selected")
        return
    print(f"SIM: {args.sim}")

    return client, args.sim


def run_sync_client(client, modbus_calls=None):
    """Run sync client."""
    _logger.info("### Client starting")
    client.connect()
    if modbus_calls:
        modbus_calls(client)
    client.close()
    _logger.info("### End of Program")


def test_calls(client):
    """Test connection works."""
    # try:
    rr = client.write_registers(0, [1, 1, 1, 0, 0, 1])
    print("#############")
    print({rr})
    # time.sleep(1)
    # rr = client.write_registers(0, [0, 0, 1, 0, 0, 1])
    rr = client.read_holding_registers(0, 6)
    print("#############")
    print({rr})
    # if rr.isError():  # pragma no cover
    #     print(f"Received Modbus library error({rr})")
    #     client.close()
    #     return
    # except Exception as exc:
    #     raise exc


async def run_async_client(client, modbus_calls=None):
    """Run sync client."""
    _logger.info("### Client starting")
    await client.connect()
    # test client is connected
    assert client.connected
    if modbus_calls:
        await modbus_calls(client)
    client.close()
    _logger.info("### End of Program")


async def atest_calls(client):
    print("get and verify data")
    rr = await client.write_registers(0, [0, 0, 1, 0, 0, 1])
    print("#############")
    print({rr})
    # try:
    # See all calls in client_calls.py
    # rr = await client.read_coils(1, 1, slave=1)
    rr = await client.read_holding_registers(0, 6)
    print("#############")
    print({rr})

    rr = await client.read_holding_registers(0, 6)
    print("#############")
    print({rr})

    rr = await client.write_registers(0, [1, 1, 1, 0, 0, 1])
    print("#############")
    print({rr})
    # except ModbusException as exc:  # pragma no cover
    #     print(f"Received ModbusException({exc}) from library")
    #     client.close()
    #     return
    if rr.isError():  # pragma no cover
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    # if isinstance(rr, ExceptionResponse):  # pragma no cover
    #     print(f"Received Modbus library exception ({rr})")
    #     # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
    #     client.close()


def main_sync(cmdline=None):
    """Combine setup and run."""
    client = setup_client(
        description="Run synchronous client.", cmdline=cmdline
    )
    run_sync_client(client, modbus_calls=test_calls)

async def main_async(cmdline=None):
    """Combine setup and run."""
    client, sim = setup_client(
        description="Run synchronous client.", cmdline=cmdline
    )
    logic = sim_async.logic1 if sim=="1" else sim_async.logic2
    await run_async_client(client, modbus_calls=logic)

if __name__ == "__main__":
    # main_sync()  # pragma: no cover
    asyncio.run(
        main_async(), debug=True
    )  # pragma: no cover

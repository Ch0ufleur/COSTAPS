#!/usr/bin/env python3
import asyncio
import logging
import time

import pymodbus.client as ModbusClient
from pymodbus import (
    pymodbus_apply_logging_config,
)

import helper
import simulation

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
        )
    elif args.comm == "tls":
        client = ModbusClient.AsyncModbusTlsClient(
            args.host,
            port=args.port,
            certfile="./certificates/pymodbus.crt",
            keyfile="./certificates/pymodbus.key",
            password="pass",
            server_hostname="localhost",
        )
    else:  # pragma no cover
        print(f"Unknown client {args.comm} selected")
        return

    return client, args.sim


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


async def test_calls(client):
    print("get and verify data")

    while True:
        rr = await client.write_coils(0, [True, False])
        print("#############")
        print(rr)
        time.sleep(3)

        rr = await client.write_coils(0, [False])
        print("#############")
        print(rr)
        time.sleep(3)

    if rr.isError():  # pragma no cover
        print(f"Received Modbus library error({rr})")
        client.close()
        return


def get_logic(sim_num):
    if sim_num == "1":
        logic = simulation.bridge_logic
    elif sim_num == "2":
        logic = simulation.intersection_logic
    elif sim_num == "3":
        logic = simulation.tbone_logic
    return logic

async def main_async(cmdline=None):
    """Combine setup and run."""
    client, sim_num = setup_client(
        description="Run synchronous client.", cmdline=cmdline
    )
    logic = get_logic(sim_num)
    await run_async_client(client, modbus_calls=logic)


if __name__ == "__main__":
    asyncio.run(
        main_async(), debug=True
    )  # pragma: no cover

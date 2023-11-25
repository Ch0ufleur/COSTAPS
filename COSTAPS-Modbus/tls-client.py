#!/usr/bin/env python3
"""Pymodbus asynchronous client example.

An example of a single threaded synchronous client.

usage: simple_client_async.py

All options must be adapted in the code
The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""
import asyncio
import logging

import pymodbus.client as ModbusClient
from pymodbus import (
    # ExceptionResponse,
    # Framer,
    # ModbusException,
    pymodbus_apply_logging_config,
)

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)


async def run_async_simple_client(comm, host, port):
    """Run async client."""
    # activate debugging
    pymodbus_apply_logging_config("DEBUG")

    print("get client")
    if comm == "tcp":
        client = ModbusClient.AsyncModbusTcpClient(
            host,
            port=port,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # source_address=("localhost", 0),
        )
    elif comm == "tls":
        client = ModbusClient.AsyncModbusTlsClient(
            host,
            port=port,
            # framer=Framer.TLS,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # sslctx=sslctx,
            certfile="./certificates/pymodbus.crt",
            keyfile="./certificates/pymodbus.key",
            password="pass",
            # server_hostname="localhost",
        )
    else:  # pragma no cover
        print(f"Unknown client {comm} selected")
        return

    print("connect to server")
    await client.connect()
    # test client is connected
    assert client.connected

    print("get and verify data")
    rr = await client.write_registers(0, [0, 0, 1, 0, 0, 1])
    # try:
    # See all calls in client_calls.py
    # rr = await client.read_coils(1, 1, slave=1)
    rr = await client.read_holding_registers(0, 2)
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

    print("close connection")
    client.close()


if __name__ == "__main__":
    asyncio.run(
        run_async_simple_client("tls", "0.0.0.0", 5020), debug=True
    )  # pragma: no cover
import argparse
import asyncio
import logging
import socket
import json
from pymodbus.server import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext

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
    def setValues(self, address, values):
        super().setValues(address % 5, values)
        print("Address changed: " + str(address % 5))
        print("Values changed: " + str(values))
        #send tcp request
        send_tcp_request(address % 5, values)
        return

# Define the Modbus slave server data
block = CustomDataBlock(0, [0] * 100)  # Create a data block with 100 registers initialized to zero
slaveContext = ModbusSlaveContext(
                di=block, co=block, hr=block, ir=block, zero_mode=True
            )
store = ModbusServerContext(slaves=slaveContext, single=True)
identity = ModbusDeviceIdentification()
identity.VendorName = 'MyCompany'
identity.ProductCode = '123'
identity.VendorUrl = 'http://www.mycompany.com'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'Modbus Server'

parser = argparse.ArgumentParser(prog='Client Modbus')
parser.add_argument('--host_modbus', default="127.0.0.1")
parser.add_argument('--port_modbus', default=502)
parser.add_argument('--host_tcp', default="127.0.0.1")
parser.add_argument('--port_tcp', default=12345)
args = parser.parse_args()
print(args.host_modbus, args.port_modbus, args.host_tcp, args.port_tcp)

# Start the Modbus TCP server
asyncio.run(StartAsyncTcpServer(store, identity=identity, address=(args.host_modbus, args.port_modbus)), debug=True)
# To stop the server, use Ctrl+C or add your custom logic to stop it
import asyncio
import logging
import socket
import json
from pymodbus.server import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext

def send_tcp_request(address, values):
    #communication server address and port
    server_address = ('127.0.0.1', 12345)
    plc_json = {
        "id": address,
        "states": [
            {
                "green": values[0],
                "yellow": values[1],
                "red": values[2]
            },
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

        # Receive the response from the server
        response_json = client_socket.recv(1024).decode()
        print(f"Received response from server: {response_json}")

class CustomDataBlock(ModbusSequentialDataBlock):
    def setValues(self, address, values):
        super().setValues(address, values)
        print("Address changed: " + str(address))
        print("Values changed: " + str(values))
        #send tcp request
        send_tcp_request(address, values)
        return 

# Define the Modbus slave server data
block = CustomDataBlock(0, [0] * 100)  # Create a data block with 100 registers initialized to zero
slaveContext = ModbusSlaveContext(
                di=block, co=block, hr=block, ir=block
            )
store = ModbusServerContext(slaves=slaveContext, single=True)
identity = ModbusDeviceIdentification()
identity.VendorName = 'MyCompany'
identity.ProductCode = '123'
identity.VendorUrl = 'http://www.mycompany.com'
identity.ProductName = 'Modbus Server'
identity.ModelName = 'Modbus Server'

# Start the Modbus TCP server
asyncio.run(StartAsyncTcpServer(store, identity=identity, address=("0.0.0.0", 502)), debug=True)   # Listening on all interfaces on port 502
# To stop the server, use Ctrl+C or add your custom logic to stop it
import asyncio
from pymodbus.server import StartAsyncTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext

class CustomDataBlock(ModbusSequentialDataBlock):
    def setValues(self, address, values):
        super().setValues(address, values)
        print("Values changed: " + str(values))
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
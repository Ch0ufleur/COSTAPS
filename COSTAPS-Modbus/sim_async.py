import logging
import time

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)

async def logic1(client):
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
            _logger.info("### Initializing SIM 1")
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(third_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.NORTBOUND_GREEN):
            _logger.info("### Northbound green")
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(third_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.MIDDLE_RED
            pastStatus = TrafficLightStates.NORTBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.MIDDLE_RED):
            _logger.info("### Middle red")
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(third_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
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
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(third_trafficlight_id, [0, 0, 1, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(fourth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(fifth_trafficlight_id, [1, 0, 0, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.MIDDLE_RED
            pastStatus = TrafficLightStates.SOUTHBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)

async def logic2(client):
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
            _logger.info("### Initializing SIM 2")
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTH_SOUTH_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.NORTH_SOUTH_GREEN):
            _logger.info("### North-South green")
            rr = await client.write_registers(first_trafficlight_id, [1, 0, 0, 1, 0, 0], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTH_SOUTH_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.NORTH_SOUTH_YELLOW):
            _logger.info("### North-South yellow")
            rr = await client.write_registers(first_trafficlight_id, [0, 1, 0, 0, 1, 0], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.ALL_RED
            pastStatus = TrafficLightStates.NORTH_SOUTH_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.ALL_RED):
            _logger.info("### All red")
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
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
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [1, 0, 0, 1, 0, 0], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.EAST_WEST_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)

        elif(currentStatus == TrafficLightStates.EAST_WEST_YELLOW):
            _logger.info("### East-West yellow")
            rr = await client.write_registers(first_trafficlight_id, [0, 0, 1, 0, 0, 1], slave=1)
            print(rr)
            rr = await client.write_registers(second_trafficlight_id, [0, 1, 0, 0, 1, 0], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.ALL_RED
            pastStatus = TrafficLightStates.EAST_WEST_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(5)
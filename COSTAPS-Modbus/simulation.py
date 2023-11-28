import logging
import time

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
_logger = logging.getLogger(__file__)
_logger.setLevel(logging.INFO)

sleep_interval = 3

async def bridge_logic(client):
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
        sleep_interval = 6
        if(currentStatus == TrafficLightStates.INITIALIZING):
            _logger.info("### Initializing Bridge Simulation (1)")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(third_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(fourth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(fifth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval)

        elif(currentStatus == TrafficLightStates.NORTBOUND_GREEN):
            _logger.info("### Northbound green")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(third_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(fourth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(fifth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.MIDDLE_RED
            pastStatus = TrafficLightStates.NORTBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval)

        elif(currentStatus == TrafficLightStates.MIDDLE_RED):
            _logger.info("### Middle red")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(third_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(fourth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(fifth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)

            if pastStatus == TrafficLightStates.SOUTHBOUND_GREEN:
                currentStatus = TrafficLightStates.NORTBOUND_GREEN
            else:
                currentStatus = TrafficLightStates.SOUTHBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval * 3)

        elif(currentStatus == TrafficLightStates.SOUTHBOUND_GREEN):
            _logger.info("### Southbound green")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(third_trafficlight_id, [False, False, True, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(fourth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(fifth_trafficlight_id, [True, False, False, False, False, True], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.MIDDLE_RED
            pastStatus = TrafficLightStates.SOUTHBOUND_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval)


async def intersection_logic(client):
    class TrafficLightStates:
        INITIALIZING = 0
        NORTH_SOUTH_GREEN = 2
        NORTH_SOUTH_YELLOW = 3
        ALL_RED = 4
        EAST_WEST_GREEN = 5
        EAST_WEST_YELLOW = 6

    first_trafficlight_id = 0 * 6
    second_trafficlight_id = 1 * 6

    currentStatus = TrafficLightStates.INITIALIZING
    pastStatus = None

    while(True):
        if(currentStatus == TrafficLightStates.INITIALIZING):
            _logger.info("### Initializing Intersection Simulation (2)")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTH_SOUTH_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval)

        elif(currentStatus == TrafficLightStates.NORTH_SOUTH_GREEN):
            _logger.info("### North-South green")
            rr = await client.write_coils(first_trafficlight_id, [True, False, False, True, False, False], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.NORTH_SOUTH_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval*3)

        elif(currentStatus == TrafficLightStates.NORTH_SOUTH_YELLOW):
            _logger.info("### North-South yellow")
            rr = await client.write_coils(first_trafficlight_id, [False, True, False, False, True, False], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.ALL_RED
            pastStatus = TrafficLightStates.NORTH_SOUTH_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval)

        elif(currentStatus == TrafficLightStates.ALL_RED):
            _logger.info("### All red")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)

            if pastStatus == TrafficLightStates.EAST_WEST_YELLOW:
                currentStatus = TrafficLightStates.NORTH_SOUTH_GREEN
            else:
                currentStatus = TrafficLightStates.EAST_WEST_GREEN

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval)

        elif(currentStatus == TrafficLightStates.EAST_WEST_GREEN):
            _logger.info("### East-West green")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [True, False, False, True, False, False], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.EAST_WEST_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval*3)

        elif(currentStatus == TrafficLightStates.EAST_WEST_YELLOW):
            _logger.info("### East-West yellow")
            rr = await client.write_coils(first_trafficlight_id, [False, False, True, False, False, True], slave=1)
            print(rr)
            rr = await client.write_coils(second_trafficlight_id, [False, True, False, False, True, False], slave=1)
            print(rr)

            currentStatus = TrafficLightStates.ALL_RED
            pastStatus = TrafficLightStates.EAST_WEST_YELLOW

            _logger.info("### Sleeping ...")
            time.sleep(sleep_interval)


async def tbone_logic(client):
    panel_id = 0 * 6

    _logger.info("### Initializing Tbone Simulation (3)")
    while(True):
        _logger.info("### All green")
        rr = await client.write_coils(panel_id, [True, False, False, True, False, False], slave=1)
        print(rr)

        _logger.info("### Sleeping ...")
        time.sleep(sleep_interval)

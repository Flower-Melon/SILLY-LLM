import time
import threading

# Task Description: Microwave a plate containing an egg and a tomato

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Place an Egg on the Plate. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Place a Tomato on the Plate. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 3: Microwave the Plate. (Skills Required: GoToObject, PickupObject, PutObject, OpenObject, CloseObject, SwitchOn, SwitchOff)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.
# SubTask 3 depends on both SubTask 1 and SubTask 2.

def place_egg_on_plate():
    # 0: SubTask 1: Place an Egg on the Plate
    # 1: Go to the Egg.
    GoToObject('Egg')
    # 2: Pick up the Egg.
    PickupObject('Egg')
    # 3: Go to the Plate.
    GoToObject('Plate')
    # 4: Put the Egg on the Plate.
    PutObject('Egg', 'Plate')

def place_tomato_on_plate():
    # 0: SubTask 2: Place a Tomato on the Plate
    # 1: Go to the Tomato.
    GoToObject('Tomato')
    # 2: Pick up the Tomato.
    PickupObject('Tomato')
    # 3: Go to the Plate.
    GoToObject('Plate')
    # 4: Put the Tomato on the Plate.
    PutObject('Tomato', 'Plate')

def microwave_plate():
    # 0: SubTask 3: Microwave the Plate
    # 1: Go to the Plate.
    GoToObject('Plate')
    # 2: Pick up the Plate.
    PickupObject('Plate')
    # 3: Go to the Microwave.
    GoToObject('Microwave')
    # 4: Open the Microwave.
    OpenObject('Microwave')
    # 5: Put the Plate inside the Microwave.
    PutObject('Plate', 'Microwave')
    # 6: Close the Microwave.
    CloseObject('Microwave')
    # 7: Switch on the Microwave.
    SwitchOn('Microwave')
    # 8: Wait for a while to let the food heat up.
    time.sleep(5)
    # 9: Switch off the Microwave.
    SwitchOff('Microwave')
    # 10: Open the Microwave.
    OpenObject('Microwave')
    # 11: Take the Plate out.
    PickupObject('Plate')
    # 12: Close the Microwave.
    CloseObject('Microwave')
    # 13: Go to the CounterTop.
    GoToObject('CounterTop')
    # 14: Put the Plate on the CounterTop.
    PutObject('Plate', 'CounterTop')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=place_egg_on_plate)
task2_thread = threading.Thread(target=place_tomato_on_plate)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Execute SubTask 3 after SubTask 1 and SubTask 2 are complete
microwave_plate()

# Task Microwave a plate containing an egg and a tomato is done

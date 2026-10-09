import time
import threading

# Task Description: Throw the cloth in trash and Fill water in the BathTub

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Throw the cloth in trash. (Skills Required: GoToObject, PickupObject, ThrowObject)
# SubTask 2: Fill water in the BathTub. (Skills Required: GoToObject, SwitchOn, SwitchOff)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# CODE
def throw_cloth_in_trash():
    # 0: SubTask 1: Throw the cloth in trash
    # 1: Go to the Cloth.
    GoToObject('Cloth')
    # 2: Pick up the Cloth.
    PickupObject('Cloth')
    # 3: Go to the GarbageCan.
    GoToObject('GarbageCan')
    # 4: Throw the Cloth into the GarbageCan.
    ThrowObject('Cloth', 'GarbageCan')

def fill_water_in_bathtub():
    # 0: SubTask 2: Fill water in the BathTub
    # 1: Go to the Bathtub.
    GoToObject('Bathtub')
    # 2: Switch on the Faucet to fill water.
    SwitchOn('Faucet')
    # 3: Wait for a while to let the Bathtub fill.
    time.sleep(5)
    # 4: Switch off the Faucet.
    SwitchOff('Faucet')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=throw_cloth_in_trash)
task2_thread = threading.Thread(target=fill_water_in_bathtub)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Throw the cloth in trash and Fill water in the BathTub is done

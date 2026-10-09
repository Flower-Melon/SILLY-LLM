import time
import threading

# Task Description: Chill the apple and wash the knife
# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Chill the apple. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# SubTask 2: Wash the knife. (Skills Required: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

def chill_apple():
    # 0: SubTask 1: Chill the apple
    # 1: Go to the Apple.
    GoToObject('Apple')
    # 2: Pick up the Apple.
    PickupObject('Apple')
    # 3: Go to the Fridge.
    GoToObject('Fridge')
    # 4: Open the Fridge.
    OpenObject('Fridge')
    # 5: Put the Apple inside the Fridge to chill.
    PutObject('Apple', 'Fridge')
    # 6: Close the Fridge.
    CloseObject('Fridge')

def wash_knife():
    # 0: SubTask 2: Wash the knife
    # 1: Go to the Knife.
    GoToObject('Knife')
    # 2: Pick up the Knife.
    PickupObject('Knife')
    # 3: Go to the Sink.
    GoToObject('Sink')
    # 4: Put the Knife inside the Sink.
    PutObject('Knife', 'Sink')
    # 5: Switch on the Faucet to wash the Knife.
    SwitchOn('Faucet')
    # 6: Wait for a while to let the Knife wash.
    time.sleep(5)
    # 7: Switch off the Faucet.
    SwitchOff('Faucet')
    # 8: Pick up the clean Knife.
    PickupObject('Knife')
    # 9: Go to the CounterTop.
    GoToObject('CounterTop')
    # 10: Place the Knife on the CounterTop.
    PutObject('Knife', 'CounterTop')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=chill_apple)
task2_thread = threading.Thread(target=wash_knife)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Chill the apple and wash the knife is done

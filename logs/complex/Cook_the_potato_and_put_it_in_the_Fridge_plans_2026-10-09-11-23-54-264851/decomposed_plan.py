import time
import threading

# Task Description: Cook the potato and put it in the Fridge

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Cook the Potato. (Skills Required: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff)
# SubTask 2: Put the cooked Potato in the Fridge. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# We can execute SubTask 1 first and then SubTask 2, since they cannot be parallelized.

# CODE
def cook_potato():
    # 0: SubTask 1: Cook the Potato
    # 1: Go to the Potato.
    GoToObject('Potato')
    # 2: Pick up the Potato.
    PickupObject('Potato')
    # 3: Go to the Pan.
    GoToObject('Pan')
    # 4: Put the Potato in the Pan.
    PutObject('Potato', 'Pan')
    # 5: Pick up the Pan with the Potato in it.
    PickupObject('Pan')
    # 6: Go to the StoveBurner.
    GoToObject('StoveBurner')
    # 7: Put the Pan on the StoveBurner.
    PutObject('Pan', 'StoveBurner')
    # 8: Switch on the StoveKnob.
    SwitchOn('StoveKnob')
    # 9: Wait for a while to let the Potato cook.
    time.sleep(5)
    # 10: Switch off the StoveKnob.
    SwitchOff('StoveKnob')
    # 11: Go to the Potato.
    GoToObject('Potato')
    # 12: Pick up the cooked Potato.
    PickupObject('Potato')

def put_potato_in_fridge():
    # 0: SubTask 2: Put the cooked Potato in the Fridge
    # 1: Go to the Fridge.
    GoToObject('Fridge')
    # 2: Open the Fridge.
    OpenObject('Fridge')
    # 3: Put the Potato inside the Fridge.
    PutObject('Potato', 'Fridge')
    # 4: Close the Fridge.
    CloseObject('Fridge')

# Execute SubTask 1
cook_potato()

# Execute SubTask 2
put_potato_in_fridge()

# Task cook the potato and put it in the Fridge is done

import threading

# Task: Slice the lettuce, trash the mug, and switch off the light.
# Decomposition:
# SubTask 1: Slice the lettuce. (GoToObject, PickupObject, SliceObject, PutObject)
# SubTask 2: Trash the mug. (GoToObject, PickupObject, PutObject)
# SubTask 3: Switch off the light. (GoToObject, SwitchOff)
# These subtasks are independent and can be parallelized.

def slice_lettuce():
    # Go to the Knife.
    GoToObject('Knife')
    # Pick up the Knife.
    PickupObject('Knife')
    # Go to the Lettuce.
    GoToObject('Lettuce')
    # Slice the Lettuce.
    SliceObject('Lettuce')
    # Go to the CounterTop.
    GoToObject('CounterTop')
    # Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

def trash_mug():
    # Go to the Mug.
    GoToObject('Mug')
    # Pick up the Mug.
    PickupObject('Mug')
    # Go to the GarbageCan.
    GoToObject('GarbageCan')
    # Put the Mug in the GarbageCan.
    PutObject('Mug', 'GarbageCan')

def switch_off_light():
    # Go to the LightSwitch.
    GoToObject('LightSwitch')
    # Switch off the LightSwitch.
    SwitchOff('LightSwitch')

# Create threads for independent subtasks.
t1 = threading.Thread(target=slice_lettuce)
t2 = threading.Thread(target=trash_mug)
t3 = threading.Thread(target=switch_off_light)

# Start all subtasks in parallel.
t1.start()
t2.start()
t3.start()

# Join all threads before finishing.
t1.join()
t2.join()
t3.join()

# Task slice the lettuce, trash the mug and switch off the light is done

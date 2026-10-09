import threading
import time

# Task: Slice the lettuce, trash the mug, and switch off the light.
# Decomposition:
# SubTask 1: Slice the lettuce. (GoToObject, PickupObject, SliceObject, PutObject)
# SubTask 2: Trash the mug. (GoToObject, PickupObject, PutObject)
# SubTask 3: Switch off the light. (GoToObject, SwitchOff)
# All robots share the same skill set, so allocation is based on mass capacity.
# robot1 (0.4) cannot handle Lettuce (0.47) or Mug (1.0).
# robot2 (2.1) handles SubTask 1; robot3 (1.0) handles SubTasks 2 & 3 sequentially.

def slice_lettuce(robot):
    # SubTask 1: Slice the lettuce using robot2.
    # Go to the Knife.
    GoToObject(robot, 'Knife')
    # Pick up the Knife.
    PickupObject(robot, 'Knife')
    # Go to the Lettuce.
    GoToObject(robot, 'Lettuce')
    # Slice the Lettuce.
    SliceObject(robot, 'Lettuce')
    # Go to the CounterTop.
    GoToObject(robot, 'CounterTop')
    # Put the Knife back on the CounterTop.
    PutObject(robot, 'Knife', 'CounterTop')

def trash_mug_and_switch_light(robot):
    # SubTask 2: Trash the mug using robot3.
    # Go to the Mug.
    GoToObject(robot, 'Mug')
    # Pick up the Mug.
    PickupObject(robot, 'Mug')
    # Go to the GarbageCan.
    GoToObject(robot, 'GarbageCan')
    # Put the Mug in the GarbageCan.
    PutObject(robot, 'Mug', 'GarbageCan')
    # SubTask 3: Switch off the light using robot3 (sequential on same robot).
    # Go to the LightSwitch.
    GoToObject(robot, 'LightSwitch')
    # Switch off the LightSwitch.
    SwitchOff(robot, 'LightSwitch')

# robot2 handles SubTask 1; robot3 handles SubTasks 2 & 3 sequentially.
t1 = threading.Thread(target=slice_lettuce, args=(robots[1]['name'],))
t2 = threading.Thread(target=trash_mug_and_switch_light, args=(robots[2]['name'],))

# Start all subtasks in parallel.
t1.start()
t2.start()

# Join all threads before finishing.
t1.join()
t2.join()

# Task slice the lettuce, trash the mug and switch off the light is done

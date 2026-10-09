import time
import threading

# Task Description: Put apple in fridge and switch off the light

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Put apple in the fridge. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# SubTask 2: Switch off the light. (Skills Required: GoToObject, SwitchOff)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

def put_apple_in_fridge(robot):
    # 0: SubTask 1: Put apple in the fridge
    # 1: Go to the Apple.
    GoToObject(robot, 'Apple')
    # 2: Pick up the Apple.
    PickupObject(robot, 'Apple')
    # 3: Go to the Fridge.
    GoToObject(robot, 'Fridge')
    # 4: Open the Fridge.
    OpenObject(robot, 'Fridge')
    # 5: Put Apple in the Fridge.
    PutObject(robot, 'Apple', 'Fridge')
    # 6: Close the Fridge.
    CloseObject(robot, 'Fridge')

def switch_off_light(robot):
    # 0: SubTask 2: Switch off the light
    # 1: Go to the LightSwitch.
    GoToObject(robot, 'LightSwitch')
    # 2: Switch off the LightSwitch.
    SwitchOff(robot, 'LightSwitch')

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]

# All robots are identical in skills and mass capacity.
# SubTask 1 requires GoToObject, PickupObject, OpenObject, PutObject, CloseObject -> robot1 has all.
# SubTask 2 requires GoToObject, SwitchOff -> robot2 has all.
# Mass checks: Apple (0.2) <= 100, LightSwitch (0.0) <= 100 -> single robots suffice.
# Subtasks are independent -> run in parallel with 2 robots.

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_apple_in_fridge, args=(robots[0]['name'],))
task2_thread = threading.Thread(target=switch_off_light, args=(robots[1]['name'],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put apple in fridge and switch off the light is done

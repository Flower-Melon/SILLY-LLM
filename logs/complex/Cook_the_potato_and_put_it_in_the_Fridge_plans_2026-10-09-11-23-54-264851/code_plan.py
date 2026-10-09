import time
import threading

# Task Description: Cook the potato and put it in the Fridge

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Cook the Potato. (Skills Required: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff)
# SubTask 2: Put the cooked Potato in the Fridge. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# SubTask 2 depends on SubTask 1, so they must be executed sequentially.

# TASK ALLOCATION
# Both robots share identical skill sets, so allocation is based on mass capacity.
# SubTask 1 requires handling Pan+Potato (0.85 mass) -> only robot1 (capacity 5) qualifies.
# SubTask 2 requires handling Potato (0.18 mass) -> only robot1 (capacity 5) qualifies.
# Both subtasks assigned to robot1, executed sequentially.

robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 5}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.02}]

def cook_potato(robot):
    # 0: SubTask 1: Cook the Potato
    # 1: Go to the Potato.
    GoToObject(robot, 'Potato')
    # 2: Pick up the Potato.
    PickupObject(robot, 'Potato')
    # 3: Go to the Pan.
    GoToObject(robot, 'Pan')
    # 4: Put the Potato in the Pan.
    PutObject(robot, 'Potato', 'Pan')
    # 5: Pick up the Pan with the Potato in it.
    PickupObject(robot, 'Pan')
    # 6: Go to the StoveBurner.
    GoToObject(robot, 'StoveBurner')
    # 7: Put the Pan on the StoveBurner.
    PutObject(robot, 'Pan', 'StoveBurner')
    # 8: Switch on the StoveKnob.
    SwitchOn(robot, 'StoveKnob')
    # 9: Wait for a while to let the Potato cook.
    time.sleep(5)
    # 10: Switch off the StoveKnob.
    SwitchOff(robot, 'StoveKnob')
    # 11: Go to the Potato.
    GoToObject(robot, 'Potato')
    # 12: Pick up the cooked Potato.
    PickupObject(robot, 'Potato')

def put_potato_in_fridge(robot):
    # 0: SubTask 2: Put the cooked Potato in the Fridge
    # 1: Go to the Fridge.
    GoToObject(robot, 'Fridge')
    # 2: Open the Fridge.
    OpenObject(robot, 'Fridge')
    # 3: Put the Potato inside the Fridge.
    PutObject(robot, 'Potato', 'Fridge')
    # 4: Close the Fridge.
    CloseObject(robot, 'Fridge')

# Execute SubTask 1 with robot1
task1_thread = threading.Thread(target=cook_potato, args=(robots[0]['name'],))
task1_thread.start()
task1_thread.join()

# Execute SubTask 2 with robot1 (depends on SubTask 1)
task2_thread = threading.Thread(target=put_potato_in_fridge, args=(robots[0]['name'],))
task2_thread.start()
task2_thread.join()

# Task cook the potato and put it in the Fridge is done

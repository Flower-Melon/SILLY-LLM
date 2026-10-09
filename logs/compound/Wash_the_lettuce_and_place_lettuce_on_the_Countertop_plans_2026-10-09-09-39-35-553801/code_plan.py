import time
import threading

# TASK ALLOCATION
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'BreakObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100},
    {'name': 'robot3', 'skills': ['GoToObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}
]

# SOLUTION
# All robots share the same mass capacity (100), which far exceeds the mass of the
# Lettuce (0.47). So mass is not a constraint; allocation is driven by skills alone.
# SubTask 1 (Wash the Lettuce) requires: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff.
#   -> robot1 and robot3 have all these skills; robot2 lacks SwitchOn/SwitchOff.
# SubTask 2 (Place the Lettuce on the Countertop) requires: GoToObject, PickupObject, PutObject.
#   -> all robots have these skills.
# SubTask 2 depends on SubTask 1 (lettuce must be washed first), so they run sequentially.
# Minimum number of robots = 1. Choose robot3 since it has all skills for both subtasks.
# No teams required.

def wash_lettuce(robot_list):
    # robot_list = [robot3]
    # 0: SubTask 1: Wash the Lettuce
    # 1: Go to the Lettuce using robot3.
    GoToObject(robot_list[0], 'Lettuce')
    # 2: Pick up the Lettuce using robot3.
    PickupObject(robot_list[0], 'Lettuce')
    # 3: Go to the Sink using robot3.
    GoToObject(robot_list[0], 'Sink')
    # 4: Put the Lettuce inside the Sink using robot3.
    PutObject(robot_list[0], 'Lettuce', 'Sink')
    # 5: Switch on the Faucet to clean the Lettuce using robot3.
    SwitchOn(robot_list[0], 'Faucet')
    # 6: Wait for a while to let the Lettuce clean.
    time.sleep(5)
    # 7: Switch off the Faucet using robot3.
    SwitchOff(robot_list[0], 'Faucet')
    # 8: Pick up the clean Lettuce using robot3.
    PickupObject(robot_list[0], 'Lettuce')

def place_lettuce_on_countertop(robot_list):
    # robot_list = [robot3]
    # 0: SubTask 2: Place the Lettuce on the Countertop
    # 1: Go to the CounterTop using robot3.
    GoToObject(robot_list[0], 'CounterTop')
    # 2: Place the Lettuce on the CounterTop using robot3.
    PutObject(robot_list[0], 'Lettuce', 'CounterTop')

# Execute SubTask 1 with robot3
task1_thread = threading.Thread(target=wash_lettuce, args=([robots[2]],))
task1_thread.start()
# SubTask 2 depends on SubTask 1, so join before proceeding.
task1_thread.join()

# Execute SubTask 2 with robot3
task2_thread = threading.Thread(target=place_lettuce_on_countertop, args=([robots[2]],))
task2_thread.start()
task2_thread.join()

# Task Wash the lettuce and place lettuce on the Countertop is done

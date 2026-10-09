import time
import threading

# Task Description: Break a vase and Turn on TV
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Break a Vase. (Skills Required: GoToObject, BreakObject)
# SubTask 2: Turn on the TV. (Skills Required: GoToObject, SwitchOn)
# These subtasks are independent and can be parallelized.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# SOLUTION
# All robots share the same set and number of skills and the same mass capacity.
# All objects have mass well below the robots' mass capacity (100).
# Therefore any single robot can perform either subtask alone. No teams are required.
# SubTask 1 (Break a Vase) requires GoToObject + BreakObject -> assign to robot1.
# SubTask 2 (Turn on the TV) requires GoToObject + SwitchOn -> assign to robot2.
# The subtasks are independent, so they are executed in parallel on two robots.

def break_vase(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Break a Vase
    # 1: Go to the Vase using robot1.
    GoToObject(robot_list[0], 'Vase')
    # 2: Break the Vase using robot1.
    BreakObject(robot_list[0], 'Vase')

def turn_on_tv(robot_list):
    # robot_list = [robot2]
    # 0: SubTask 2: Turn on the TV
    # 1: Go to the Television using robot2.
    GoToObject(robot_list[0], 'Television')
    # 2: Switch on the Television using robot2.
    SwitchOn(robot_list[0], 'Television')

# Parallelize SubTask 1 and SubTask 2 on two different robots
task1_thread = threading.Thread(target=break_vase, args=([robots[0]],))
task2_thread = threading.Thread(target=turn_on_tv, args=([robots[1]],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Break a vase and Turn on TV is done

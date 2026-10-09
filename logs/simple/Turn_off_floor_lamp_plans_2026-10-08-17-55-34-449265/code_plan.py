import time
import threading

# Task Description: Turn off floor lamp
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Turn off the FloorLamp. (Skills Required: GoToObject, SwitchOff)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# Both robots possess the required skills (GoToObject, SwitchOff) and sufficient mass capacity.
# Only one subtask exists, so only one robot is needed. Assign SubTask 1 to robot1.

def turn_off_floor_lamp(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Turn off the FloorLamp
    # 1: Go to the FloorLamp using robot1.
    GoToObject(robot_list[0], 'FloorLamp')
    # 2: Switch off the FloorLamp using robot1.
    SwitchOff(robot_list[0], 'FloorLamp')

# Perform SubTask 1 with robot1
task1_thread = threading.Thread(target=turn_off_floor_lamp, args=([robots[0]],))
# Start executing SubTask 1
task1_thread.start()
# Join the task thread before finishing
task1_thread.join()
# Task turn off floor lamp is done

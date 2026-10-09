import time
import threading

# Task Description: Turn on the laptop

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Turn on the laptop. (Skills Required: GoToObject, SwitchOn)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]

# SOLUTION
# Only one robot is available. It possesses both required skills (GoToObject, SwitchOn)
# and has ample mass capacity (100 >= 2.3 for the Laptop). No team is required.
# The single subtask is assigned to robot1.

def turn_on_laptop(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Turn on the laptop
    # 1: Go to the Laptop using robot1.
    GoToObject(robot_list[0], 'Laptop')
    # 2: Switch on the Laptop using robot1.
    SwitchOn(robot_list[0], 'Laptop')

# Perform SubTask 1 with robot1
task1_thread = threading.Thread(target=turn_on_laptop, args=([robots[0]],))
# Start executing SubTask 1
task1_thread.start()

# Join all task threads before finishing
task1_thread.join()

# Task turn on the laptop is done

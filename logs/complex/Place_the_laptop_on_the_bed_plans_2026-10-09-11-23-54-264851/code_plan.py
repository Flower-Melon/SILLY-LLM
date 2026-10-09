import time
import threading

# Task Description: Place the laptop on the bed
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Place the laptop on the bed. (Skills Required: GoToObject, PickupObject, PutObject)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 5}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.4}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.08}]
# SOLUTION
# All robots share the same set and number of skills, so allocation is based on mass alone.
# The Laptop has mass 2.3 and must be picked up. The Bed (mass 30.0) is only a receptacle, so its mass is irrelevant.
# Only robot1 has mass_capacity (5) >= 2.3. Robot2 (0.4) and robot3 (0.08) cannot lift the Laptop.
# No team is required since robot1 alone satisfies both skill and mass requirements.
# The 'Place the laptop on the bed' subtask is assigned to robot1.

# Code Solution
def place_laptop_on_bed(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Place the laptop on the bed
    # 1: Go to the Laptop using robot1.
    GoToObject(robot_list[0], 'Laptop')
    # 2: Pick up the Laptop using robot1.
    PickupObject(robot_list[0], 'Laptop')
    # 3: Go to the Bed using robot1.
    GoToObject(robot_list[0], 'Bed')
    # 4: Put the Laptop on the Bed using robot1.
    PutObject(robot_list[0], 'Laptop', 'Bed')

# Perform SubTask 1 with robot1
task1_thread = threading.Thread(target=place_laptop_on_bed, args=([robots[0]],))
# Start executing SubTask 1
task1_thread.start()
# Join the task thread before finishing
task1_thread.join()
# Task Place the laptop on the bed is done

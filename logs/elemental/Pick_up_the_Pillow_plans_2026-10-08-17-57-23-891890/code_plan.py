import time
import threading

# Task Description: Pick up the Pillow
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Pick up the Pillow. (Skills Required: GoToObject, PickupObject)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.4}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.08}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 1.0}, {'name': 'robot4', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.02}]

# SOLUTION
# All robots share the same set and number of skills, so skill requirements are satisfied by every robot.
# The differentiator is mass capacity. The Pillow has mass ~0.7.
# Only robot3 has mass_capacity (1.0) >= 0.7. Robots 1, 2, and 4 have insufficient capacity.
# No team is needed since robot3 alone satisfies both skill and mass requirements.
# SubTask 1 is assigned to robot3.

def pick_up_pillow(robot_list):
    # robot_list = [robot3]
    # 0: SubTask 1: Pick up the Pillow
    # 1: Go to the Pillow using robot3.
    GoToObject(robot_list[0], 'Pillow')
    # 2: Pick up the Pillow using robot3.
    PickupObject(robot_list[0], 'Pillow')

# Perform SubTask 1 with robot3
task1_thread = threading.Thread(target=pick_up_pillow, args=([robots[2]],))
# Start executing SubTask 1
task1_thread.start()
# Join the task thread before finishing
task1_thread.join()

# Task Pick up the Pillow is done

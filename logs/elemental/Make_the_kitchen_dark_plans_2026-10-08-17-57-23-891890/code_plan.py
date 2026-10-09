import time
import threading

# Task Description: Make the kitchen dark
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Turn off the LightSwitch. (Skills Required: GoToObject, SwitchOff)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# SOLUTION
# Only one robot is available. robot1 possesses both required skills (GoToObject, SwitchOff).
# The only object involved is the LightSwitch (mass = 0.0), well within robot1's mass capacity of 100.
# No team is required. SubTask 1 is assigned to robot1.

def make_kitchen_dark(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Turn off the LightSwitch
    # 1: Go to the LightSwitch using robot1.
    GoToObject(robot_list[0], 'LightSwitch')
    # 2: Switch off the LightSwitch to make the kitchen dark using robot1.
    SwitchOff(robot_list[0], 'LightSwitch')

# Perform SubTask 1 with robot1
task1_thread = threading.Thread(target=make_kitchen_dark, args=([robots[0]],))
# Start executing SubTask 1
task1_thread.start()
# Join the task thread before finishing
task1_thread.join()
# Task make the kitchen dark is done

import time
import threading

# Task Description: Fill water in the BathTub
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Fill water in the BathTub. (Skills Required: GoToObject, SwitchOn, SwitchOff)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# Only one robot is available. It possesses all required skills (GoToObject, SwitchOn, SwitchOff).
# The objects involved (Bathtub, Faucet) have mass 0.0, well within robot1's mass capacity of 100.
# No team formation or parallelization is required; robot1 alone can perform the single subtask.

def fill_bathtub(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Fill water in the BathTub
    # 1: Go to the Bathtub using robot1.
    GoToObject(robot_list[0], 'Bathtub')
    # 2: Switch on the Faucet to fill the Bathtub with water using robot1.
    SwitchOn(robot_list[0], 'Faucet')
    # 3: Wait for a while to let the Bathtub fill with water.
    time.sleep(5)
    # 4: Switch off the Faucet using robot1.
    SwitchOff(robot_list[0], 'Faucet')

# Perform SubTask 1 with robot1
task1_thread = threading.Thread(target=fill_bathtub, args=([robots[0]],))
# Start executing SubTask 1
task1_thread.start()
# Join the task thread before finishing
task1_thread.join()
# Task Fill water in the BathTub is done

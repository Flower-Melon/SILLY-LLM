import time
import threading

# Task Description: Put mug in coffee machine

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Put the Mug in the CoffeeMachine. (Skills Required: GoToObject, PickupObject, PutObject)
# We can execute SubTask 1 directly.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# All robots share the same set of skills and there is only one robot available.
# The Mug has mass 1.0, which is well within robot1's mass capacity of 100.
# robot1 possesses all required skills: GoToObject, PickupObject, PutObject.
# No team is required since a single robot can perform the entire subtask.

def put_mug_in_coffee_machine(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Put the Mug in the CoffeeMachine
    # 1: Go to the Mug using robot1.
    GoToObject(robot_list[0], 'Mug')
    # 2: Pick up the Mug using robot1.
    PickupObject(robot_list[0], 'Mug')
    # 3: Go to the CoffeeMachine using robot1.
    GoToObject(robot_list[0], 'CoffeeMachine')
    # 4: Put the Mug in the CoffeeMachine using robot1.
    PutObject(robot_list[0], 'Mug', 'CoffeeMachine')

# Perform SubTask 1 with robot1
task1_thread = threading.Thread(target=put_mug_in_coffee_machine, args=([robots[0]],))
# Start executing SubTask 1
task1_thread.start()

# Join all task threads before finishing
task1_thread.join()

# Task put mug in coffee machine is done

import threading
import time

# Task Description: put mug in the coffee machine and switch on the coffee machine

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Put the Mug in the CoffeeMachine. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Switch on the CoffeeMachine. (Skills Required: GoToObject, SwitchOn)
# SubTask 2 depends on SubTask 1 (mug must be placed before switching on), so execute sequentially.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'BreakObject', 'ThrowObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100}]
# All robots have different skill sets, so allocate based on skills alone.
# SubTask 1 requires GoToObject, PickupObject, PutObject -> only robot1 has all three.
# SubTask 2 requires GoToObject, SwitchOn -> only robot3 has both.
# Mug mass = 1.0 <= robot1 capacity (100). CoffeeMachine is not lifted, so mass is not a constraint.
# No teams required; each subtask is covered by a single robot.

def put_mug_in_coffee_machine(robot):
    # 0: SubTask 1: Put the Mug in the CoffeeMachine
    # 1: Go to the Mug.
    GoToObject(robot, 'Mug')
    # 2: Pick up the Mug.
    PickupObject(robot, 'Mug')
    # 3: Go to the CoffeeMachine.
    GoToObject(robot, 'CoffeeMachine')
    # 4: Put the Mug in the CoffeeMachine.
    PutObject(robot, 'Mug', 'CoffeeMachine')

def switch_on_coffee_machine(robot):
    # 0: SubTask 2: Switch on the CoffeeMachine
    # 1: Go to the CoffeeMachine.
    GoToObject(robot, 'CoffeeMachine')
    # 2: Switch on the CoffeeMachine.
    SwitchOn(robot, 'CoffeeMachine')

# Execute SubTask 1 with robot1
task1_thread = threading.Thread(target=put_mug_in_coffee_machine, args=(robots[0]['name'],))
task1_thread.start()
# Join SubTask 1 before starting SubTask 2 due to dependency
task1_thread.join()

# Execute SubTask 2 with robot3
task2_thread = threading.Thread(target=switch_on_coffee_machine, args=(robots[2]['name'],))
task2_thread.start()
task2_thread.join()

# Task put mug in the coffee machine and switch on the coffee machine is done

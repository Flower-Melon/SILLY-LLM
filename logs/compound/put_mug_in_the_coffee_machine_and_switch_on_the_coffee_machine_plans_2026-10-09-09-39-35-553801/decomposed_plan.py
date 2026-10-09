import threading

# Task Description: put mug in the coffee machine and switch on the coffee machine

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Put the Mug in the CoffeeMachine. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Switch on the CoffeeMachine. (Skills Required: GoToObject, SwitchOn)
# SubTask 2 depends on SubTask 1 because the mug must be placed before switching on.
# Therefore, execute SubTask 1 first, then SubTask 2.

def put_mug_in_coffee_machine():
    # 0: SubTask 1: Put the Mug in the CoffeeMachine
    # 1: Go to the Mug.
    GoToObject('Mug')
    # 2: Pick up the Mug.
    PickupObject('Mug')
    # 3: Go to the CoffeeMachine.
    GoToObject('CoffeeMachine')
    # 4: Put the Mug in the CoffeeMachine.
    PutObject('Mug', 'CoffeeMachine')

def switch_on_coffee_machine():
    # 0: SubTask 2: Switch on the CoffeeMachine
    # 1: Go to the CoffeeMachine.
    GoToObject('CoffeeMachine')
    # 2: Switch on the CoffeeMachine.
    SwitchOn('CoffeeMachine')

# Execute SubTask 1
put_mug_in_coffee_machine()

# Execute SubTask 2 after SubTask 1 is complete
switch_on_coffee_machine()

# Task put mug in the coffee machine and switch on the coffee machine is done

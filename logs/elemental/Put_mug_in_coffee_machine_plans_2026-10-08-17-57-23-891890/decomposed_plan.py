# Task Description: Put mug in coffee machine

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Put the Mug in the CoffeeMachine. (Skills Required: GoToObject, PickupObject, PutObject)
# We can execute SubTask 1 directly.

# CODE
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

# Execute SubTask 1
put_mug_in_coffee_machine()

# Task put mug in coffee machine is done

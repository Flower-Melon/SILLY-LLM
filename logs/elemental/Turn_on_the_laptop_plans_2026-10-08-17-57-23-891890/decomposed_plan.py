# Task Description: Turn on the laptop

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Turn on the laptop. (Skills Required: GoToObject, SwitchOn)
# We can execute SubTask 1.

# CODE
def turn_on_laptop():
    # 0: SubTask 1: Turn on the laptop
    # 1: Go to the Laptop.
    GoToObject('Laptop')
    # 2: Switch on the Laptop.
    SwitchOn('Laptop')

# Execute SubTask 1
turn_on_laptop()

# Task turn on the laptop is done

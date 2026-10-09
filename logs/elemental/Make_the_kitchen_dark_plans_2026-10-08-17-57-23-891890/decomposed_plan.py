# Task Description: Make the kitchen dark

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Turn off the LightSwitch. (Skills Required: GoToObject, SwitchOff)
# We can execute SubTask 1.

# CODE
def make_kitchen_dark():
    # 0: SubTask 1: Turn off the LightSwitch
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch off the LightSwitch to make the kitchen dark.
    SwitchOff('LightSwitch')

# Execute SubTask 1
make_kitchen_dark()

# Task make the kitchen dark is done

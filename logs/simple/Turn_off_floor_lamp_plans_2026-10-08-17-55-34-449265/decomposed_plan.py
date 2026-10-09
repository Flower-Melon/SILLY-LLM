# Task Description: Turn off floor lamp

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Turn off the FloorLamp. (Skills Required: GoToObject, SwitchOff)
# We can execute SubTask 1.

# CODE
def turn_off_floor_lamp():
    # 0: SubTask 1: Turn off the FloorLamp
    # 1: Go to the FloorLamp.
    GoToObject('FloorLamp')
    # 2: Switch off the FloorLamp.
    SwitchOff('FloorLamp')

# Execute SubTask 1
turn_off_floor_lamp()

# Task turn off floor lamp is done

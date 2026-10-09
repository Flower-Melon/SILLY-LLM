# Task Description: Open the Laptop and Turn it ON.

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Open the Laptop. (Skills Required: GoToObject, OpenObject)
# SubTask 2: Turn the Laptop ON. (Skills Required: GoToObject, SwitchOn)
# These subtasks are sequential because the laptop must be opened before it can be turned on.

# CODE
def open_and_turn_on_laptop():
    # 0: SubTask 1: Open the Laptop
    # 1: Go to the Laptop.
    GoToObject('Laptop')
    # 2: Open the Laptop.
    OpenObject('Laptop')
    # 3: SubTask 2: Turn the Laptop ON
    # 4: Switch on the Laptop.
    SwitchOn('Laptop')

# Execute the task
open_and_turn_on_laptop()

# Task Open the Laptop and Turn it ON is done

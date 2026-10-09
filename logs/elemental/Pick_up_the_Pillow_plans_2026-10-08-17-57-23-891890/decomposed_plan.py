# Task Description: Pick up the Pillow

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Pick up the Pillow. (Skills Required: GoToObject, PickupObject)
# We can execute SubTask 1.

# CODE
def pick_up_pillow():
    # 0: SubTask 1: Pick up the Pillow
    # 1: Go to the Pillow.
    GoToObject('Pillow')
    # 2: Pick up the Pillow.
    PickupObject('Pillow')

# Execute SubTask 1
pick_up_pillow()

# Task Pick up the Pillow is done

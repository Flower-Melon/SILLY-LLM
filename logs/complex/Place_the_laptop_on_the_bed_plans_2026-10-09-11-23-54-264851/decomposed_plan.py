# Task Description: Place the laptop on the bed

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Place the laptop on the bed. (Skills Required: GoToObject, PickupObject, PutObject)
# We can execute SubTask 1.

# CODE
def place_laptop_on_bed():
    # 0: SubTask 1: Place the laptop on the bed
    # 1: Go to the Laptop.
    GoToObject('Laptop')
    # 2: Pick up the Laptop.
    PickupObject('Laptop')
    # 3: Go to the Bed.
    GoToObject('Bed')
    # 4: Put the Laptop on the Bed.
    PutObject('Laptop', 'Bed')

# Execute SubTask 1
place_laptop_on_bed()

# Task Place the laptop on the bed is done

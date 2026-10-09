# Task Description: Put the vase on the sofa

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Put the vase on the sofa. (Skills Required: GoToObject, PickupObject, PutObject)
# We can execute SubTask 1.

# CODE
def put_vase_on_sofa():
    # 0: SubTask 1: Put the vase on the sofa
    # 1: Go to the Vase.
    GoToObject('Vase')
    # 2: Pick up the Vase.
    PickupObject('Vase')
    # 3: Go to the Sofa.
    GoToObject('Sofa')
    # 4: Put the Vase on the Sofa.
    PutObject('Vase', 'Sofa')

# Execute SubTask 1
put_vase_on_sofa()

# Task put the vase on the sofa is done

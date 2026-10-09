import threading

# Task Description: Put the Box on the sofa and the bowl in the box

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Put the Box on the Sofa. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Put the Bowl in the Box. (Skills Required: GoToObject, PickupObject, PutObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

def put_box_on_sofa():
    # 0: SubTask 1: Put the Box on the Sofa
    # 1: Go to the Box.
    GoToObject('Box')
    # 2: Pick up the Box.
    PickupObject('Box')
    # 3: Go to the Sofa.
    GoToObject('Sofa')
    # 4: Put the Box on the Sofa.
    PutObject('Box', 'Sofa')

def put_bowl_in_box():
    # 0: SubTask 2: Put the Bowl in the Box
    # 1: Go to the Bowl.
    GoToObject('Bowl')
    # 2: Pick up the Bowl.
    PickupObject('Bowl')
    # 3: Go to the Box.
    GoToObject('Box')
    # 4: Put the Bowl in the Box.
    PutObject('Bowl', 'Box')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_box_on_sofa)
task2_thread = threading.Thread(target=put_bowl_in_box)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put the Box on the sofa and the bowl in the box is done

import threading

# Task Description: Break the Cellphone and Close the blinds

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Break the Cellphone. (Skills Required: GoToObject, BreakObject)
# SubTask 2: Close the Blinds. (Skills Required: GoToObject, CloseObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# CODE
def break_cellphone():
    # 0: SubTask 1: Break the Cellphone
    # 1: Go to the CellPhone.
    GoToObject('CellPhone')
    # 2: Break the CellPhone.
    BreakObject('CellPhone')

def close_blinds():
    # 0: SubTask 2: Close the Blinds
    # 1: Go to the Blinds.
    GoToObject('Blinds')
    # 2: Close the Blinds.
    CloseObject('Blinds')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=break_cellphone)
task2_thread = threading.Thread(target=close_blinds)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Break the Cellphone and Close the blinds is done

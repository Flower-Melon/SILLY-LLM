import threading

# Task Description: Put the baseballbat and tennis racket on the bed

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Put the BaseballBat on the Bed. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Put the TennisRacket on the Bed. (Skills Required: GoToObject, PickupObject, PutObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# CODE
def put_baseballbat_on_bed():
    # 0: SubTask 1: Put the BaseballBat on the Bed
    # 1: Go to the BaseballBat.
    GoToObject('BaseballBat')
    # 2: Pick up the BaseballBat.
    PickupObject('BaseballBat')
    # 3: Go to the Bed.
    GoToObject('Bed')
    # 4: Put the BaseballBat on the Bed.
    PutObject('BaseballBat', 'Bed')

def put_tennisracket_on_bed():
    # 0: SubTask 2: Put the TennisRacket on the Bed
    # 1: Go to the TennisRacket.
    GoToObject('TennisRacket')
    # 2: Pick up the TennisRacket.
    PickupObject('TennisRacket')
    # 3: Go to the Bed.
    GoToObject('Bed')
    # 4: Put the TennisRacket on the Bed.
    PutObject('TennisRacket', 'Bed')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_baseballbat_on_bed)
task2_thread = threading.Thread(target=put_tennisracket_on_bed)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put the baseballbat and tennis racket on the bed is done

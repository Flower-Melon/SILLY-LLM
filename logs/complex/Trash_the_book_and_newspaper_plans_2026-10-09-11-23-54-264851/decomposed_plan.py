import threading

# Task Description: Trash the book and newspaper
# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Trash the Book. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Trash the Newspaper. (Skills Required: GoToObject, PickupObject, PutObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

def trash_book():
    # 0: SubTask 1: Trash the Book
    # 1: Go to the Book.
    GoToObject('Book')
    # 2: Pick up the Book.
    PickupObject('Book')
    # 3: Go to the GarbageCan.
    GoToObject('GarbageCan')
    # 4: Put the Book in the GarbageCan.
    PutObject('Book', 'GarbageCan')

def trash_newspaper():
    # 0: SubTask 2: Trash the Newspaper
    # 1: Go to the Newspaper.
    GoToObject('Newspaper')
    # 2: Pick up the Newspaper.
    PickupObject('Newspaper')
    # 3: Go to the GarbageCan.
    GoToObject('GarbageCan')
    # 4: Put the Newspaper in the GarbageCan.
    PutObject('Newspaper', 'GarbageCan')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=trash_book)
task2_thread = threading.Thread(target=trash_newspaper)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Trash the book and newspaper is done

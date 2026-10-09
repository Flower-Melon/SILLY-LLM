import time
import threading

# Task Description: Put the book in the box and Turn on the mobile phone

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Put the book in the box. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Turn on the mobile phone. (Skills Required: GoToObject, PickupObject, SwitchOn)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

def put_book_in_box():
    # 0: SubTask 1: Put the book in the box
    # 1: Go to the Book.
    GoToObject('Book')
    # 2: Pick up the Book.
    PickupObject('Book')
    # 3: Go to the Box.
    GoToObject('Box')
    # 4: Put the Book inside the Box.
    PutObject('Book', 'Box')

def turn_on_mobile_phone():
    # 0: SubTask 2: Turn on the mobile phone
    # 1: Go to the CellPhone.
    GoToObject('CellPhone')
    # 2: Pick up the CellPhone.
    PickupObject('CellPhone')
    # 3: Switch on the CellPhone.
    SwitchOn('CellPhone')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_book_in_box)
task2_thread = threading.Thread(target=turn_on_mobile_phone)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put the book in the box and Turn on the mobile phone is done

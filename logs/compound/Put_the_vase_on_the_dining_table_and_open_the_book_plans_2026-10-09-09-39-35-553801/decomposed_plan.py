import threading

# Task Description: Put the vase on the dining table and open the book.
# Decompose into independent subtasks that can be parallelized:
# SubTask 1: Put the vase on the dining table. (GoToObject, PickupObject, PutObject)
# SubTask 2: Open the book. (GoToObject, OpenObject)
# These subtasks are independent, so run them in parallel.

def put_vase_on_dining_table():
    # 1: Go to the Vase.
    GoToObject('Vase')
    # 2: Pick up the Vase.
    PickupObject('Vase')
    # 3: Go to the DiningTable.
    GoToObject('DiningTable')
    # 4: Put the Vase on the DiningTable.
    PutObject('Vase', 'DiningTable')

def open_book():
    # 1: Go to the Book.
    GoToObject('Book')
    # 2: Open the Book.
    OpenObject('Book')

# Parallelize the two independent subtasks.
task1_thread = threading.Thread(target=put_vase_on_dining_table)
task2_thread = threading.Thread(target=open_book)

# Start executing both subtasks in parallel.
task1_thread.start()
task2_thread.start()

# Wait for both subtasks to finish.
task1_thread.join()
task2_thread.join()

# Task Put the vase on the dining table and open the book is done

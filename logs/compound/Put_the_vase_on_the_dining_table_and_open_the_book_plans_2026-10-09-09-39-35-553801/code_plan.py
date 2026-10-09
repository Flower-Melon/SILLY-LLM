import threading

# Task: Put the vase on the dining table and open the book.
# Decompose into two independent subtasks that can run in parallel:
#   SubTask 1: Put the vase on the dining table. (GoToObject, PickupObject, PutObject)
#   SubTask 2: Open the book. (GoToObject, OpenObject)
# Robots:
#   robot1: GoToObject, PickupObject, PutObject (mass_capacity 100)
#   robot2: GoToObject, OpenObject, CloseObject (mass_capacity 100)
# SubTask 1 requires PickupObject/PutObject -> only robot1 has them.
# SubTask 2 requires OpenObject -> only robot2 has it.
# Mass check: Vase 1.0 <= 100, Book 0.5 <= 100. No teams needed.

def put_vase_on_dining_table(robot):
    # SubTask 1: Put the vase on the dining table (robot1)
    # 1: Go to the Vase.
    GoToObject(robot, 'Vase')
    # 2: Pick up the Vase.
    PickupObject(robot, 'Vase')
    # 3: Go to the DiningTable.
    GoToObject(robot, 'DiningTable')
    # 4: Put the Vase on the DiningTable.
    PutObject(robot, 'Vase', 'DiningTable')

def open_book(robot):
    # SubTask 2: Open the book (robot2)
    # 1: Go to the Book.
    GoToObject(robot, 'Book')
    # 2: Open the Book.
    OpenObject(robot, 'Book')

# Assign subtasks to robots based on skills.
task1_thread = threading.Thread(target=put_vase_on_dining_table, args=(robots[0]['name'],))
task2_thread = threading.Thread(target=open_book, args=(robots[1]['name'],))

# Start executing both subtasks in parallel.
task1_thread.start()
task2_thread.start()

# Join all task threads before finishing.
task1_thread.join()
task2_thread.join()

# Task Put the vase on the dining table and open the book is done

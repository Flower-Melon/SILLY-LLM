import threading

# Task Description: Put the watch in the box and watering can on the coffeetable.
# Decompose into independent subtasks that can be parallelized:
# SubTask 1: Put the watch in the box. (GoToObject, PickupObject, PutObject)
# SubTask 2: Put the watering can on the coffeetable. (GoToObject, PickupObject, PutObject)
# These subtasks are independent, so run them in parallel.

def put_watch_in_box():
    # Go to the watch.
    GoToObject('Watch')
    # Pick up the watch.
    PickupObject('Watch')
    # Go to the box.
    GoToObject('Box')
    # Put the watch inside the box.
    PutObject('Watch', 'Box')

def put_watering_can_on_coffeetable():
    # Go to the watering can.
    GoToObject('WateringCan')
    # Pick up the watering can.
    PickupObject('WateringCan')
    # Go to the coffee table.
    GoToObject('CoffeeTable')
    # Put the watering can on the coffee table.
    PutObject('WateringCan', 'CoffeeTable')

# Create threads for the two independent subtasks.
task1_thread = threading.Thread(target=put_watch_in_box)
task2_thread = threading.Thread(target=put_watering_can_on_coffeetable)

# Start both subtasks in parallel.
task1_thread.start()
task2_thread.start()

# Wait for both subtasks to finish.
task1_thread.join()
task2_thread.join()

# Task complete: watch is in the box and watering can is on the coffee table.

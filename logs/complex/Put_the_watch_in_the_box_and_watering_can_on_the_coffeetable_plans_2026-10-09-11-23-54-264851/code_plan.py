import threading

# Task: Put the watch in the box and watering can on the coffeetable.
# Decompose into two independent subtasks that can run in parallel:
#   SubTask 1: Put the watch in the box. (GoToObject, PickupObject, PutObject)
#   SubTask 2: Put the watering can on the coffeetable. (GoToObject, PickupObject, PutObject)
#
# TASK ALLOCATION:
# Both robots share the same skill set, so allocation is driven by mass capacity.
#   SubTask 1: heaviest picked object = Watch (0.07). robot2 capacity 0.08 >= 0.07 -> robot2.
#   SubTask 2: heaviest picked object = WateringCan (1.0). robot2 capacity 0.08 < 1.0,
#              robot1 capacity 2.1 >= 1.0 -> robot1.
# No teams required; each subtask is handled by a single capable robot.

def put_watch_in_box(robot):
    # Go to the watch.
    GoToObject(robot, 'Watch')
    # Pick up the watch.
    PickupObject(robot, 'Watch')
    # Go to the box.
    GoToObject(robot, 'Box')
    # Put the watch inside the box.
    PutObject(robot, 'Watch', 'Box')

def put_watering_can_on_coffeetable(robot):
    # Go to the watering can.
    GoToObject(robot, 'WateringCan')
    # Pick up the watering can.
    PickupObject(robot, 'WateringCan')
    # Go to the coffee table.
    GoToObject(robot, 'CoffeeTable')
    # Put the watering can on the coffee table.
    PutObject(robot, 'WateringCan', 'CoffeeTable')

# SubTask 1 -> robot2 (mass 0.07 <= 0.08)
# SubTask 2 -> robot1 (mass 1.0 <= 2.1)
task1_thread = threading.Thread(target=put_watch_in_box, args=(robots[1],))
task2_thread = threading.Thread(target=put_watering_can_on_coffeetable, args=(robots[0],))

# Start both subtasks in parallel.
task1_thread.start()
task2_thread.start()

# Join all task threads before finishing.
task1_thread.join()
task2_thread.join()

# Task complete: watch is in the box and watering can is on the coffee table.

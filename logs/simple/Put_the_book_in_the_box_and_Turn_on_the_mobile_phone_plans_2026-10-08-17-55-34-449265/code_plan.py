import time
import threading

# Task Description: Put the book in the box and Turn on the mobile phone

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Put the book in the box. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Turn on the mobile phone. (Skills Required: GoToObject, PickupObject, SwitchOn)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot4', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# SOLUTION
# All robots share the same set and number of skills and the same mass capacity.
# Allocation is driven purely by parallelism: two independent subtasks -> use 2 robots in parallel.
# SubTask 1 (Put book in box) requires GoToObject, PickupObject, PutObject -> robot1 has all.
# SubTask 2 (Turn on mobile phone) requires GoToObject, PickupObject, SwitchOn -> robot2 has all.
# Mass check: Book 0.5, CellPhone 0.16, both <= 100. No teams required.

def put_book_in_box(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Put the book in the box
    # 1: Go to the Book using robot1.
    GoToObject(robot_list[0], 'Book')
    # 2: Pick up the Book using robot1.
    PickupObject(robot_list[0], 'Book')
    # 3: Go to the Box using robot1.
    GoToObject(robot_list[0], 'Box')
    # 4: Put the Book inside the Box using robot1.
    PutObject(robot_list[0], 'Book', 'Box')

def turn_on_mobile_phone(robot_list):
    # robot_list = [robot2]
    # 0: SubTask 2: Turn on the mobile phone
    # 1: Go to the CellPhone using robot2.
    GoToObject(robot_list[0], 'CellPhone')
    # 2: Pick up the CellPhone using robot2.
    PickupObject(robot_list[0], 'CellPhone')
    # 3: Switch on the CellPhone using robot2.
    SwitchOn(robot_list[0], 'CellPhone')

# Parallelize SubTask 1 and SubTask 2 on two separate robots
task1_thread = threading.Thread(target=put_book_in_box, args=([robots[0]],))
task2_thread = threading.Thread(target=turn_on_mobile_phone, args=([robots[1]],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put the book in the box and Turn on the mobile phone is done

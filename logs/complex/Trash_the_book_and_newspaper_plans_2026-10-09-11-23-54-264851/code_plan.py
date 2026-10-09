import threading

# Task Description: Trash the book and newspaper
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Trash the Book. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Trash the Newspaper. (Skills Required: GoToObject, PickupObject, PutObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.4}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 5}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.02}, {'name': 'robot4', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.9}]
# All robots share the same skill set, so skills are not a constraint.
# Mass is the differentiator: Book mass = 0.5, Newspaper mass = 0.2.
# robot2 (5.0) and robot4 (0.9) can carry both objects; robot1 (0.4) and robot3 (0.02) cannot.
# Assign SubTask 1 (Book) to robot2 and SubTask 2 (Newspaper) to robot4, run in parallel.

def trash_book(robot_list):
    # robot_list = [robot2]
    # 0: SubTask 1: Trash the Book
    # 1: Go to the Book using robot2.
    GoToObject(robot_list[0], 'Book')
    # 2: Pick up the Book using robot2.
    PickupObject(robot_list[0], 'Book')
    # 3: Go to the GarbageCan using robot2.
    GoToObject(robot_list[0], 'GarbageCan')
    # 4: Put the Book in the GarbageCan using robot2.
    PutObject(robot_list[0], 'Book', 'GarbageCan')

def trash_newspaper(robot_list):
    # robot_list = [robot4]
    # 0: SubTask 2: Trash the Newspaper
    # 1: Go to the Newspaper using robot4.
    GoToObject(robot_list[0], 'Newspaper')
    # 2: Pick up the Newspaper using robot4.
    PickupObject(robot_list[0], 'Newspaper')
    # 3: Go to the GarbageCan using robot4.
    GoToObject(robot_list[0], 'GarbageCan')
    # 4: Put the Newspaper in the GarbageCan using robot4.
    PutObject(robot_list[0], 'Newspaper', 'GarbageCan')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=trash_book, args=([robots[1]],))
task2_thread = threading.Thread(target=trash_newspaper, args=([robots[3]],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Trash the book and newspaper is done

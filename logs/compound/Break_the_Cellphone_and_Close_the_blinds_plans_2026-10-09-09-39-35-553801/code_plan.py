import threading

# Task Description: Break the Cellphone and Close the blinds

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Break the Cellphone. (Skills Required: GoToObject, BreakObject)
# SubTask 2: Close the Blinds. (Skills Required: GoToObject, CloseObject)
# These subtasks are independent and can be parallelized.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'SliceObject', 'PickupObject'], 'mass_capacity': 100}]
# SubTask 1 (Break the Cellphone) requires GoToObject and BreakObject -> robot2 has both.
# SubTask 2 (Close the Blinds) requires GoToObject and CloseObject -> robot1 has both.
# Mass capacities are sufficient (100 >= 0.16 and 100 >= 0.0). No teams required.

def break_cellphone(robot_list):
    # robot_list = [robot2]
    # 0: SubTask 1: Break the Cellphone
    # 1: Go to the CellPhone using robot2.
    GoToObject(robot_list[0], 'CellPhone')
    # 2: Break the CellPhone using robot2.
    BreakObject(robot_list[0], 'CellPhone')

def close_blinds(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 2: Close the Blinds
    # 1: Go to the Blinds using robot1.
    GoToObject(robot_list[0], 'Blinds')
    # 2: Close the Blinds using robot1.
    CloseObject(robot_list[0], 'Blinds')

# Parallelize SubTask 1 and SubTask 2 on separate robots
task1_thread = threading.Thread(target=break_cellphone, args=([robots[1]],))
task2_thread = threading.Thread(target=close_blinds, args=([robots[0]],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Break the Cellphone and Close the blinds is done

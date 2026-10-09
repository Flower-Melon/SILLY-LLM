import threading

# Task Description: Put the baseballbat and tennis racket on the bed

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Put the BaseballBat on the Bed. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Put the TennisRacket on the Bed. (Skills Required: GoToObject, PickupObject, PutObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# Both robots share the same set and number of skills and the same mass capacity.
# Both subtasks require GoToObject, PickupObject, PutObject and involve small masses (BaseballBat=0.9, TennisRacket=0.31),
# well within the mass capacity of either robot. No skill gap and no mass gap -> no teams required.
# SubTask 1 and SubTask 2 are independent -> assign one subtask per robot and run in parallel.

def put_baseballbat_on_bed(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Put the BaseballBat on the Bed
    # 1: Go to the BaseballBat using robot1.
    GoToObject(robot_list[0], 'BaseballBat')
    # 2: Pick up the BaseballBat using robot1.
    PickupObject(robot_list[0], 'BaseballBat')
    # 3: Go to the Bed using robot1.
    GoToObject(robot_list[0], 'Bed')
    # 4: Put the BaseballBat on the Bed using robot1.
    PutObject(robot_list[0], 'BaseballBat', 'Bed')

def put_tennisracket_on_bed(robot_list):
    # robot_list = [robot2]
    # 0: SubTask 2: Put the TennisRacket on the Bed
    # 1: Go to the TennisRacket using robot2.
    GoToObject(robot_list[0], 'TennisRacket')
    # 2: Pick up the TennisRacket using robot2.
    PickupObject(robot_list[0], 'TennisRacket')
    # 3: Go to the Bed using robot2.
    GoToObject(robot_list[0], 'Bed')
    # 4: Put the TennisRacket on the Bed using robot2.
    PutObject(robot_list[0], 'TennisRacket', 'Bed')

# Parallelize SubTask 1 (robot1) and SubTask 2 (robot2)
task1_thread = threading.Thread(target=put_baseballbat_on_bed, args=([robots[0]],))
task2_thread = threading.Thread(target=put_tennisracket_on_bed, args=([robots[1]],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put the baseballbat and tennis racket on the bed is done

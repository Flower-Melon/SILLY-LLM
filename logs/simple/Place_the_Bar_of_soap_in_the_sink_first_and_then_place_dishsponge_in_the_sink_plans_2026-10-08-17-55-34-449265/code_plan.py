import threading
import time

# Task Description: Place the Bar of soap in the sink first and then place dishsponge in the sink

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Place the Bar of soap in the sink. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Place the dishsponge in the sink. (Skills Required: GoToObject, PickupObject, PutObject)
# We cannot parallelize SubTask 1 and SubTask 2 because the task requires the soap to be placed first.

# TASK ALLOCATION
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100},
    {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}
]

# SOLUTION
# All robots share the same set and number of skills and the same mass capacity.
# Both subtasks require GoToObject, PickupObject, PutObject skills, which every robot has.
# Masses involved (SoapBar 0.11, DishSponge 0.03) are far below any robot's capacity (100).
# No skill gap and no mass gap -> no team formation needed.
# Subtasks are sequential ("first...then"), so we use the minimum number of robots = 1.
# Assign both subtasks to robot1, executed sequentially.

def place_soap_in_sink(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Place the Bar of soap in the sink
    # 1: Go to the SoapBar using robot1.
    GoToObject(robot_list[0], 'SoapBar')
    # 2: Pick up the SoapBar using robot1.
    PickupObject(robot_list[0], 'SoapBar')
    # 3: Go to the Sink using robot1.
    GoToObject(robot_list[0], 'Sink')
    # 4: Put the SoapBar in the Sink using robot1.
    PutObject(robot_list[0], 'SoapBar', 'Sink')

def place_dishsponge_in_sink(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 2: Place the dishsponge in the sink
    # 1: Go to the DishSponge using robot1.
    GoToObject(robot_list[0], 'DishSponge')
    # 2: Pick up the DishSponge using robot1.
    PickupObject(robot_list[0], 'DishSponge')
    # 3: Go to the Sink using robot1.
    GoToObject(robot_list[0], 'Sink')
    # 4: Put the DishSponge in the Sink using robot1.
    PutObject(robot_list[0], 'DishSponge', 'Sink')

# Execute SubTask 1 first with robot1
task1_thread = threading.Thread(target=place_soap_in_sink, args=([robots[0]],))
task1_thread.start()
task1_thread.join()

# Execute SubTask 2 after SubTask 1 is complete with robot1
task2_thread = threading.Thread(target=place_dishsponge_in_sink, args=([robots[0]],))
task2_thread.start()
task2_thread.join()

# Task Place the Bar of soap in the sink first and then place dishsponge in the sink is done

import time
import threading

# Task Description: Slice the tomato

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Slice the Tomato. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]

# SOLUTION
# All robots share the same set and number of skills and all have equal mass capacity (100).
# The heaviest object handled is the Knife (0.18), well within every robot's capacity.
# All robots possess the required skills: GoToObject, PickupObject, SliceObject, PutObject.
# The subtask is a single indivisible sequence (hold knife -> slice -> return knife),
# so it cannot be split across robots. Minimum robots needed = 1.
# Assign SubTask 1 to robot1.

def slice_tomato(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Slice the Tomato
    # 1: Go to the Knife using robot1.
    GoToObject(robot_list[0], 'Knife')
    # 2: Pick up the Knife using robot1.
    PickupObject(robot_list[0], 'Knife')
    # 3: Go to the Tomato using robot1.
    GoToObject(robot_list[0], 'Tomato')
    # 4: Slice the Tomato using robot1.
    SliceObject(robot_list[0], 'Tomato')
    # 5: Go to the CounterTop using robot1.
    GoToObject(robot_list[0], 'CounterTop')
    # 6: Put the Knife back on the CounterTop using robot1.
    PutObject(robot_list[0], 'Knife', 'CounterTop')

# Perform SubTask 1 with robot1
task1_thread = threading.Thread(target=slice_tomato, args=([robots[0]],))
# Start executing SubTask 1
task1_thread.start()
# Join all task threads before finishing
task1_thread.join()

# Task slice the tomato is done

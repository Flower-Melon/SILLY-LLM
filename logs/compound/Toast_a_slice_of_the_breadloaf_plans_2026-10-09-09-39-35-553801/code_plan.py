import time
import threading

# Task Description: Toast a slice of the breadloaf

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Slice the Bread. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
# SubTask 2: Toast the Bread slice. (Skills Required: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff)
# SubTask 2 depends on SubTask 1 (bread must be sliced before toasting), so they run sequentially.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'SliceObject', 'PickupObject'], 'mass_capacity': 100}]
# All robots have different skill sets. Focus on Task Allocation based on Robot Skills alone.
# SubTask 1 requires {GoToObject, PickupObject, SliceObject, PutObject}. No single robot has all skills.
#   Team {robot2, robot3} covers all required skills (robot3: GoToObject, PickupObject, SliceObject; robot2: GoToObject, PutObject).
# SubTask 2 requires {GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff}. No single robot has all skills.
#   Team {robot1, robot2} covers all required skills (robot2: GoToObject, PickupObject, PutObject; robot1: GoToObject, SwitchOn, SwitchOff).
# Mass of all handled objects (max 0.7 kg) is far below every robot's capacity (100), so mass is not a constraint.
# Teams are required since SubTasks can't be performed by individual robots.

def slice_bread(robot_list):
    # robot_list = [robot2, robot3]
    # 0: SubTask 1: Slice the Bread
    # 1: Go to the Knife using robot3.
    GoToObject(robot_list[1], 'Knife')
    # 2: Pick up the Knife using robot3.
    PickupObject(robot_list[1], 'Knife')
    # 3: Go to the Bread using robot3.
    GoToObject(robot_list[1], 'Bread')
    # 4: Slice the Bread using robot3.
    SliceObject(robot_list[1], 'Bread')
    # 5: Go to the CounterTop using robot2.
    GoToObject(robot_list[0], 'CounterTop')
    # 6: Put the Knife back on the CounterTop using robot2.
    PutObject(robot_list[0], 'Knife', 'CounterTop')

def toast_bread(robot_list):
    # robot_list = [robot1, robot2]
    # 0: SubTask 2: Toast the Bread slice
    # 1: Go to the sliced Bread using robot2.
    GoToObject(robot_list[1], 'Bread')
    # 2: Pick up the sliced Bread using robot2.
    PickupObject(robot_list[1], 'Bread')
    # 3: Go to the Toaster using robot2.
    GoToObject(robot_list[1], 'Toaster')
    # 4: Put the sliced Bread in the Toaster using robot2.
    PutObject(robot_list[1], 'Bread', 'Toaster')
    # 5: Switch on the Toaster using robot1.
    SwitchOn(robot_list[0], 'Toaster')
    # 6: Wait for a while to let the Bread toast.
    time.sleep(5)
    # 7: Switch off the Toaster using robot1.
    SwitchOff(robot_list[0], 'Toaster')
    # 8: Go to the Bread using robot2.
    GoToObject(robot_list[1], 'Bread')
    # 9: Pick up the toasted Bread using robot2.
    PickupObject(robot_list[1], 'Bread')
    # 10: Go to the Plate using robot2.
    GoToObject(robot_list[1], 'Plate')
    # 11: Put the toasted Bread on the Plate using robot2.
    PutObject(robot_list[1], 'Bread', 'Plate')

# Execute SubTask 1 with team {robot2, robot3}
task1_thread = threading.Thread(target=slice_bread, args=([robots[1], robots[2]],))
task1_thread.start()
task1_thread.join()

# Execute SubTask 2 with team {robot1, robot2} after SubTask 1 completes
task2_thread = threading.Thread(target=toast_bread, args=([robots[0], robots[1]],))
task2_thread.start()
task2_thread.join()

# Task toast a slice of the breadloaf is done

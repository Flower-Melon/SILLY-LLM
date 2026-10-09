import time
import threading

# Task Description: Open the Laptop and Turn it ON.

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Open the Laptop. (Skills Required: GoToObject, OpenObject)
# SubTask 2: Turn the Laptop ON. (Skills Required: GoToObject, SwitchOn)
# These subtasks are sequential because the laptop must be opened before it can be turned on.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject'], 'mass_capacity': 100}]
# SOLUTION
# All robots have different sets of skills. Focus on Task Allocation based on Robot Skills alone.
# SubTask 1 (Open the Laptop) requires 'GoToObject' and 'OpenObject'. Only robot3 has both skills.
# SubTask 2 (Turn the Laptop ON) requires 'GoToObject' and 'SwitchOn'. Only robot1 has both skills.
# Mass of the Laptop (2.3) is far below every robot's capacity (100), so mass is not a constraint.
# The subtasks are sequential (laptop must be opened before it can be switched on), so they run one after another.
# No teams are required since each subtask can be performed by an individual robot.
# SubTask 1 is assigned to robot3, SubTask 2 is assigned to robot1.

# Code Solution
def open_laptop(robot_list):
    # robot_list = [robot3]
    # 0: SubTask 1: Open the Laptop
    # 1: Go to the Laptop using robot3.
    GoToObject(robot_list[0], 'Laptop')
    # 2: Open the Laptop using robot3.
    OpenObject(robot_list[0], 'Laptop')

def turn_on_laptop(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 2: Turn the Laptop ON
    # 1: Go to the Laptop using robot1.
    GoToObject(robot_list[0], 'Laptop')
    # 2: Switch on the Laptop using robot1.
    SwitchOn(robot_list[0], 'Laptop')

# Perform SubTask 1 with robot3
task1_thread = threading.Thread(target=open_laptop, args=([robots[2]],))
# Start executing SubTask 1
task1_thread.start()
# Join SubTask 1 before starting SubTask 2 (sequential dependency)
task1_thread.join()

# Perform SubTask 2 with robot1
task2_thread = threading.Thread(target=turn_on_laptop, args=([robots[0]],))
# Start executing SubTask 2
task2_thread.start()
# Join SubTask 2 before finishing
task2_thread.join()

# Task Open the Laptop and Turn it ON is done

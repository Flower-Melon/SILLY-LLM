import threading
import time

# Task Description: Put plunger in cabinet and Turn off the light.
# Decompose into independent subtasks that can be parallelized:
# SubTask 1: Put the Plunger in the Cabinet. (Skills: GoToObject, PickupObject, PutObject)
# SubTask 2: Turn off the Light. (Skills: GoToObject, SwitchOff)
# These subtasks are independent, so run them in parallel.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100}]
# All robots DONOT share the same set of skills. Focus on Task Allocation based on Robot Skills alone.
# SubTask 1 requires GoToObject, PickupObject, PutObject -> robot2 has all these skills (mass of Plunger 1.0 <= 100).
# SubTask 2 requires GoToObject, SwitchOff -> robot1 has all these skills (mass of LightSwitch 0.0 <= 100).
# No teams required; each subtask maps to a single robot. Run in parallel.

def put_plunger_in_cabinet(robot_list):
    # robot_list = [robot2]
    # 0: SubTask 1: Put the Plunger in the Cabinet
    # 1: Go to the Plunger using robot2.
    GoToObject(robot_list[0], 'Plunger')
    # 2: Pick up the Plunger using robot2.
    PickupObject(robot_list[0], 'Plunger')
    # 3: Go to the Cabinet using robot2.
    GoToObject(robot_list[0], 'Cabinet')
    # 4: Put the Plunger inside the Cabinet using robot2.
    PutObject(robot_list[0], 'Plunger', 'Cabinet')

def turn_off_light(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 2: Turn off the Light
    # 1: Go to the LightSwitch using robot1.
    GoToObject(robot_list[0], 'LightSwitch')
    # 2: Switch off the LightSwitch using robot1.
    SwitchOff(robot_list[0], 'LightSwitch')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_plunger_in_cabinet, args=([robots[1]],))
task2_thread = threading.Thread(target=turn_off_light, args=([robots[0]],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put plunger in cabinet and Turn off the light is done

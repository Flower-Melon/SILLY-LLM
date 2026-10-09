import time
import threading

# Task: Put the vase on the sofa
# Decomposition: single subtask requiring GoToObject, PickupObject, PutObject.
# Mass gap: Vase mass = 1.0; robot1 cap = 0.4, robot2 cap = 0.9 -> neither alone suffices.
# Team {robot1, robot2}: combined capacity 1.3 >= 1.0, combined skills cover all required.

robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.4},
    {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 0.9}
]

def put_vase_on_sofa(robot_list):
    # robot_list = [robot1, robot2] working cooperatively
    # 0: SubTask 1: Put the Vase on the Sofa
    # 1: Go to the Vase using the team.
    GoToObject(robot_list, 'Vase')
    # 2: Pick up the Vase using the team (combined capacity 1.3 >= 1.0).
    PickupObject(robot_list, 'Vase')
    # 3: Go to the Sofa using the team.
    GoToObject(robot_list, 'Sofa')
    # 4: Put the Vase on the Sofa using the team.
    PutObject(robot_list, 'Vase', 'Sofa')

# Execute SubTask 1 with the team of robot1 and robot2
task1_thread = threading.Thread(target=put_vase_on_sofa, args=([robots[0], robots[1]],))
task1_thread.start()

# Join all task threads before finishing
task1_thread.join()

# Task put the vase on the sofa is done

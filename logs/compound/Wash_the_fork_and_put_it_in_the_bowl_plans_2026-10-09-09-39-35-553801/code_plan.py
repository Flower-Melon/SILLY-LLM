import time
import threading

# Task: Wash the fork and put it in the bowl
# Subtasks are sequential (SubTask 2 depends on SubTask 1).
# SubTask 1 (Wash Fork) requires: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff
#   -> No single robot has all skills. Team {robot2, robot3} covers all required skills.
# SubTask 2 (Put Fork in Bowl) requires: GoToObject, PickupObject, PutObject
#   -> robot3 alone has all skills.
# Mass is not a constraint (all objects << 100).

robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'BreakObject', 'ThrowObject'], 'mass_capacity': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100},
    {'name': 'robot3', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100}
]


def wash_fork(robot_list):
    # robot_list = [robot2, robot3]
    # robot2 handles faucet switching; robot3 handles fork manipulation.
    # 1: Go to the Fork using robot3.
    GoToObject(robot_list[1], 'Fork')
    # 2: Pick up the Fork using robot3.
    PickupObject(robot_list[1], 'Fork')
    # 3: Go to the Sink using robot3.
    GoToObject(robot_list[1], 'Sink')
    # 4: Put the Fork inside the Sink using robot3.
    PutObject(robot_list[1], 'Fork', 'Sink')
    # 5: Switch on the Faucet to clean the Fork using robot2.
    SwitchOn(robot_list[0], 'Faucet')
    # 6: Wait for a while to let the Fork clean.
    time.sleep(5)
    # 7: Switch off the Faucet using robot2.
    SwitchOff(robot_list[0], 'Faucet')
    # 8: Pick up the clean Fork using robot3.
    PickupObject(robot_list[1], 'Fork')


def put_fork_in_bowl(robot_list):
    # robot_list = [robot3]
    # 1: Go to the Bowl using robot3.
    GoToObject(robot_list[0], 'Bowl')
    # 2: Put the Fork inside the Bowl using robot3.
    PutObject(robot_list[0], 'Fork', 'Bowl')


# Execute SubTask 1 with team {robot2, robot3}
task1_thread = threading.Thread(target=wash_fork, args=([robots[1], robots[2]],))
task1_thread.start()
task1_thread.join()  # SubTask 2 depends on SubTask 1 completing

# Execute SubTask 2 with robot3
task2_thread = threading.Thread(target=put_fork_in_bowl, args=([robots[2]],))
task2_thread.start()
task2_thread.join()

# Task Wash the fork and put it in the bowl is done

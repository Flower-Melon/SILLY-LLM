import threading
import time

# Task: Turn on Sink faucet and put toilet paper in the trash
# Decomposition:
#   SubTask 1: Turn on the Sink faucet. (Skills: GoToObject, SwitchOn)
#   SubTask 2: Put toilet paper in the trash. (Skills: GoToObject, PickupObject, PutObject)
# These subtasks are independent -> run in parallel.

# TASK ALLOCATION
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject'], 'mass_capacity': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100},
    {'name': 'robot3', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100},
    {'name': 'robot4', 'skills': ['GoToObject', 'SliceObject', 'PickupObject'], 'mass_capacity': 100},
]

# All robots have mass_capacity 100, far exceeding any object mass (max 0.7).
# Mass is not a constraint -> allocation is driven purely by skills.
# SubTask 1 requires GoToObject + SwitchOn -> only robot2 has both.
# SubTask 2 requires GoToObject + PickupObject + PutObject -> only robot3 has all three.
# No teams required; each subtask maps to a single robot.

def turn_on_sink_faucet(robot):
    # SubTask 1: Turn on the Sink faucet (assigned to robot2)
    # 1: Go to the Sink.
    GoToObject(robot, 'Sink')
    # 2: Switch on the Faucet.
    SwitchOn(robot, 'Faucet')

def put_toilet_paper_in_trash(robot):
    # SubTask 2: Put toilet paper in the trash (assigned to robot3)
    # 1: Go to the ToiletPaper.
    GoToObject(robot, 'ToiletPaper')
    # 2: Pick up the ToiletPaper.
    PickupObject(robot, 'ToiletPaper')
    # 3: Go to the GarbageCan.
    GoToObject(robot, 'GarbageCan')
    # 4: Put the ToiletPaper in the GarbageCan.
    PutObject(robot, 'ToiletPaper', 'GarbageCan')

# Parallelize SubTask 1 (robot2) and SubTask 2 (robot3)
task1_thread = threading.Thread(target=turn_on_sink_faucet, args=(robots[1]['name'],))
task2_thread = threading.Thread(target=put_toilet_paper_in_trash, args=(robots[2]['name'],))

# Start executing both subtasks in parallel
task1_thread.start()
task2_thread.start()

# Join all task threads before finishing
task1_thread.join()
task2_thread.join()

# Task Turn on Sink faucet and put toilet paper in the trash is done

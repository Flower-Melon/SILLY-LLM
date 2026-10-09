import time
import threading

# Task Description: Throw the cloth in trash and Fill water in the BathTub

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Throw the cloth in trash. (Skills Required: GoToObject, PickupObject, ThrowObject)
# SubTask 2: Fill water in the BathTub. (Skills Required: GoToObject, SwitchOn, SwitchOff)
# The subtasks are logically independent, but only one robot is available,
# so they must be executed sequentially on that single robot.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}]
# Only one robot exists. It possesses all required skills
# (GoToObject, PickupObject, ThrowObject, SwitchOn, SwitchOff) and its
# mass capacity (100) far exceeds the heaviest object (GarbageCan, 0.7).
# No team formation is needed. Since a single robot cannot run two subtasks
# simultaneously, the subtasks are serialized on robot1.

# Code Solution
def throw_cloth_in_trash(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 1: Throw the cloth in trash
    # 1: Go to the Cloth using robot1.
    GoToObject(robot_list[0], 'Cloth')
    # 2: Pick up the Cloth using robot1.
    PickupObject(robot_list[0], 'Cloth')
    # 3: Go to the GarbageCan using robot1.
    GoToObject(robot_list[0], 'GarbageCan')
    # 4: Throw the Cloth into the GarbageCan using robot1.
    ThrowObject(robot_list[0], 'Cloth', 'GarbageCan')

def fill_water_in_bathtub(robot_list):
    # robot_list = [robot1]
    # 0: SubTask 2: Fill water in the BathTub
    # 1: Go to the Bathtub using robot1.
    GoToObject(robot_list[0], 'Bathtub')
    # 2: Switch on the Faucet to fill water using robot1.
    SwitchOn(robot_list[0], 'Faucet')
    # 3: Wait for a while to let the Bathtub fill using robot1.
    time.sleep(5)
    # 4: Switch off the Faucet using robot1.
    SwitchOff(robot_list[0], 'Faucet')

# Execute SubTask 1 with robot1
task1_thread = threading.Thread(target=throw_cloth_in_trash, args=([robots[0]],))
# Execute SubTask 2 with robot1
task2_thread = threading.Thread(target=fill_water_in_bathtub, args=([robots[0]],))

# Start executing SubTask 1 and SubTask 2 (serialized on the single robot)
task1_thread.start()
task1_thread.join()
task2_thread.start()
task2_thread.join()

# Task Throw the cloth in trash and Fill water in the BathTub is done

import time
import threading

# Task Description: Microwave a plate containing an egg and a tomato

# GENERAL TASK DECOMPOSITION
# SubTask 1: Place an Egg on the Plate. (Skills: GoToObject, PickupObject, PutObject)
# SubTask 2: Place a Tomato on the Plate. (Skills: GoToObject, PickupObject, PutObject)
# SubTask 3: Microwave the Plate. (Skills: GoToObject, PickupObject, PutObject, OpenObject, CloseObject, SwitchOn, SwitchOff)
# SubTask 1 and SubTask 2 are independent but both require robot3, so they are serialized.
# SubTask 3 depends on SubTask 1 and SubTask 2.

# TASK ALLOCATION
# robot1: GoToObject, OpenObject, CloseObject
# robot2: GoToObject, SwitchOn, SwitchOff
# robot3: GoToObject, PickupObject, PutObject
# robot4: GoToObject, SliceObject, PickupObject (not needed)
# SubTask 1 -> robot3
# SubTask 2 -> robot3
# SubTask 3 -> team {robot1, robot2, robot3}

def place_egg_on_plate(robot):
    # 0: SubTask 1: Place an Egg on the Plate
    # 1: Go to the Egg.
    GoToObject(robot, 'Egg')
    # 2: Pick up the Egg.
    PickupObject(robot, 'Egg')
    # 3: Go to the Plate.
    GoToObject(robot, 'Plate')
    # 4: Put the Egg on the Plate.
    PutObject(robot, 'Egg', 'Plate')

def place_tomato_on_plate(robot):
    # 0: SubTask 2: Place a Tomato on the Plate
    # 1: Go to the Tomato.
    GoToObject(robot, 'Tomato')
    # 2: Pick up the Tomato.
    PickupObject(robot, 'Tomato')
    # 3: Go to the Plate.
    GoToObject(robot, 'Plate')
    # 4: Put the Tomato on the Plate.
    PutObject(robot, 'Tomato', 'Plate')

def microwave_plate(robot_list):
    # robot_list = [robot1, robot2, robot3]
    # 0: SubTask 3: Microwave the Plate
    # 1: Go to the Plate using robot3.
    GoToObject(robot_list[2], 'Plate')
    # 2: Pick up the Plate using robot3.
    PickupObject(robot_list[2], 'Plate')
    # 3: Go to the Microwave using robot3.
    GoToObject(robot_list[2], 'Microwave')
    # 4: Open the Microwave using robot1.
    OpenObject(robot_list[0], 'Microwave')
    # 5: Put the Plate inside the Microwave using robot3.
    PutObject(robot_list[2], 'Plate', 'Microwave')
    # 6: Close the Microwave using robot1.
    CloseObject(robot_list[0], 'Microwave')
    # 7: Switch on the Microwave using robot2.
    SwitchOn(robot_list[1], 'Microwave')
    # 8: Wait for a while to let the food heat up.
    time.sleep(5)
    # 9: Switch off the Microwave using robot2.
    SwitchOff(robot_list[1], 'Microwave')
    # 10: Open the Microwave using robot1.
    OpenObject(robot_list[0], 'Microwave')
    # 11: Take the Plate out using robot3.
    PickupObject(robot_list[2], 'Plate')
    # 12: Close the Microwave using robot1.
    CloseObject(robot_list[0], 'Microwave')
    # 13: Go to the CounterTop using robot3.
    GoToObject(robot_list[2], 'CounterTop')
    # 14: Put the Plate on the CounterTop using robot3.
    PutObject(robot_list[2], 'Plate', 'CounterTop')

# Execute SubTask 1 (robot3)
place_egg_on_plate(robots[2])

# Execute SubTask 2 (robot3) after SubTask 1
place_tomato_on_plate(robots[2])

# Execute SubTask 3 with team {robot1, robot2, robot3}
microwave_plate([robots[0], robots[1], robots[2]])

# Task Microwave a plate containing an egg and a tomato is done

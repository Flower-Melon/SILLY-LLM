import threading

# Task Description: Put the Box on the sofa and the bowl in the box

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Put the Box on the Sofa. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Put the Bowl in the Box. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2 depends on SubTask 1 (the Box must be placed on the Sofa before the Bowl can be put inside it),
# so they must run sequentially.

# TASK ALLOCATION
# Both robots share the same skill set. Focus on mass capacity.
# SubTask 1 lifts the Box (mass 0.30): robot1 (0.4) OK, robot2 (1.0) OK.
# SubTask 2 lifts the Bowl (mass 0.47): robot1 (0.4) FAILS, robot2 (1.0) OK.
# Since robot2 can perform both subtasks alone, minimum robots = 1 (robot2).

def put_box_on_sofa(robot):
    # 0: SubTask 1: Put the Box on the Sofa
    # 1: Go to the Box.
    GoToObject(robot, 'Box')
    # 2: Pick up the Box.
    PickupObject(robot, 'Box')
    # 3: Go to the Sofa.
    GoToObject(robot, 'Sofa')
    # 4: Put the Box on the Sofa.
    PutObject(robot, 'Box', 'Sofa')

def put_bowl_in_box(robot):
    # 0: SubTask 2: Put the Bowl in the Box
    # 1: Go to the Bowl.
    GoToObject(robot, 'Bowl')
    # 2: Pick up the Bowl.
    PickupObject(robot, 'Bowl')
    # 3: Go to the Box.
    GoToObject(robot, 'Box')
    # 4: Put the Bowl in the Box.
    PutObject(robot, 'Bowl', 'Box')

# Sequential execution on robot2 (minimum robots = 1)
task1_thread = threading.Thread(target=put_box_on_sofa, args=(robots[1],))
task1_thread.start()
task1_thread.join()

task2_thread = threading.Thread(target=put_bowl_in_box, args=(robots[1],))
task2_thread.start()
task2_thread.join()

# Task Put the Box on the sofa and the bowl in the box is done

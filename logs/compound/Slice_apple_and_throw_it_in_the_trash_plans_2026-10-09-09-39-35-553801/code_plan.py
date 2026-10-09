import time
import threading

# Task Description: Slice apple and throw it in the trash
# Decompose into sequential subtasks:
# SubTask 1: Slice the Apple. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
# SubTask 2: Throw the Apple slices in the trash. (Skills Required: GoToObject, PickupObject, ThrowObject)
# These subtasks are dependent, so execute sequentially.

robots = [{'name': 'robot1', 'skills': ['GoToObject', 'SliceObject', 'PickupObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'BreakObject', 'ThrowObject'], 'mass_capacity': 100}]

# SubTask 1 assigned to team {robot1, robot2}:
#   robot2 handles GoToObject/PickupObject/PutObject (knife handling)
#   robot1 handles SliceObject (the actual slicing)
# SubTask 2 assigned to team {robot1, robot3}:
#   robot1 handles GoToObject/PickupObject (grab the apple slices)
#   robot3 handles ThrowObject (throw into trash)

def slice_apple(robot_list):
    # robot_list = [robot1, robot2]
    # 0: SubTask 1: Slice the Apple
    # 1: Go to the Knife using robot2.
    GoToObject(robot_list[1], 'Knife')
    # 2: Pick up the Knife using robot2.
    PickupObject(robot_list[1], 'Knife')
    # 3: Go to the Apple using robot2.
    GoToObject(robot_list[1], 'Apple')
    # 4: Slice the Apple using robot1.
    SliceObject(robot_list[0], 'Apple')
    # 5: Go to the CounterTop using robot2.
    GoToObject(robot_list[1], 'CounterTop')
    # 6: Put the Knife back on the CounterTop using robot2.
    PutObject(robot_list[1], 'Knife', 'CounterTop')

def throw_apple_in_trash(robot_list):
    # robot_list = [robot1, robot3]
    # 0: SubTask 2: Throw the Apple slices in the trash
    # 1: Go to the sliced Apple using robot1.
    GoToObject(robot_list[0], 'Apple')
    # 2: Pick up the Apple slices using robot1.
    PickupObject(robot_list[0], 'Apple')
    # 3: Go to the GarbageCan using robot3.
    GoToObject(robot_list[1], 'GarbageCan')
    # 4: Throw the Apple slices into the trash using robot3.
    ThrowObject(robot_list[1], 'Apple', 'GarbageCan')

# Execute SubTask 1 with team {robot1, robot2}
task1_thread = threading.Thread(target=slice_apple, args=([robots[0], robots[1]],))
task1_thread.start()
# Join SubTask 1 before starting SubTask 2 (sequential dependency)
task1_thread.join()

# Execute SubTask 2 with team {robot1, robot3}
task2_thread = threading.Thread(target=throw_apple_in_trash, args=([robots[0], robots[2]],))
task2_thread.start()
task2_thread.join()

# Task slice apple and throw it in the trash is done

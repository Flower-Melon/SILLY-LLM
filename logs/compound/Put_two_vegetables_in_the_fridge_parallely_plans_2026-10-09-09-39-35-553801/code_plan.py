import threading
import time

# Task: Put two vegetables in the fridge in parallel.
# Available vegetables: Lettuce, Tomato, Potato. We choose Lettuce and Tomato.
# Two independent subtasks -> run in parallel on two capable robots.

# TASK ALLOCATION
robots = [
    {'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100},
    {'name': 'robot2', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100},
    {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100},
    {'name': 'robot4', 'skills': ['GoToObject', 'BreakObject', 'ThrowObject'], 'mass_capacity': 100}
]

# Required skills for each subtask: GoToObject, PickupObject, OpenObject, PutObject, CloseObject
# robot1 and robot3 have all required skills; robot2 and robot4 do not.
# Mass: Lettuce=0.47, Tomato=0.12, both far below capacity 100 -> mass not a constraint.
# Assign SubTask 1 (Lettuce) to robot1, SubTask 2 (Tomato) to robot3, run in parallel.

def put_lettuce_in_fridge(robot):
    # SubTask 1: Put the Lettuce in the Fridge using robot1
    GoToObject(robot, 'Lettuce')          # go to the lettuce
    PickupObject(robot, 'Lettuce')        # pick it up
    GoToObject(robot, 'Fridge')           # go to the fridge
    OpenObject(robot, 'Fridge')           # open the fridge
    PutObject(robot, 'Lettuce', 'Fridge') # place lettuce inside
    CloseObject(robot, 'Fridge')          # close the fridge

def put_tomato_in_fridge(robot):
    # SubTask 2: Put the Tomato in the Fridge using robot3
    GoToObject(robot, 'Tomato')           # go to the tomato
    PickupObject(robot, 'Tomato')         # pick it up
    GoToObject(robot, 'Fridge')           # go to the fridge
    OpenObject(robot, 'Fridge')           # open the fridge
    PutObject(robot, 'Tomato', 'Fridge')  # place tomato inside
    CloseObject(robot, 'Fridge')          # close the fridge

# Create threads for the two independent subtasks
lettuce_thread = threading.Thread(target=put_lettuce_in_fridge, args=(robots[0]['name'],))
tomato_thread = threading.Thread(target=put_tomato_in_fridge, args=(robots[2]['name'],))

# Start both subtasks in parallel
lettuce_thread.start()
tomato_thread.start()

# Wait for both subtasks to finish
lettuce_thread.join()
tomato_thread.join()

# Task "Put two vegetables in the fridge parallely" is done

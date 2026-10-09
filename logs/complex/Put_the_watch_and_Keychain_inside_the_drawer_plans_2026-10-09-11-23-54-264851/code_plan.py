import threading

# Task Description: Put the watch and Keychain inside the drawer

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Put the Watch inside the Drawer. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# SubTask 2: Put the KeyChain inside the Drawer. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'OpenObject', 'CloseObject', 'BreakObject', 'SliceObject', 'SwitchOn', 'SwitchOff', 'PickupObject', 'PutObject', 'DropHandObject', 'ThrowObject', 'PushObject', 'PullObject'], 'mass_capacity': 1.0}]

# All robots share the same set and number of skills, so allocation is based on mass capacity.
# Watch mass = 0.07, KeyChain mass = 0.075. All robots satisfy these individually.
# No teams required. Assign SubTask 1 to robot1 and SubTask 2 to robot2, run in parallel.

def put_watch_in_drawer(robot):
    # 0: SubTask 1: Put the Watch inside the Drawer
    # 1: Go to the Watch.
    GoToObject(robot, 'Watch')
    # 2: Pick up the Watch.
    PickupObject(robot, 'Watch')
    # 3: Go to the Drawer.
    GoToObject(robot, 'Drawer')
    # 4: Open the Drawer.
    OpenObject(robot, 'Drawer')
    # 5: Put the Watch inside the Drawer.
    PutObject(robot, 'Watch', 'Drawer')
    # 6: Close the Drawer.
    CloseObject(robot, 'Drawer')

def put_keychain_in_drawer(robot):
    # 0: SubTask 2: Put the KeyChain inside the Drawer
    # 1: Go to the KeyChain.
    GoToObject(robot, 'KeyChain')
    # 2: Pick up the KeyChain.
    PickupObject(robot, 'KeyChain')
    # 3: Go to the Drawer.
    GoToObject(robot, 'Drawer')
    # 4: Open the Drawer.
    OpenObject(robot, 'Drawer')
    # 5: Put the KeyChain inside the Drawer.
    PutObject(robot, 'KeyChain', 'Drawer')
    # 6: Close the Drawer.
    CloseObject(robot, 'Drawer')

# Parallelize SubTask 1 (robot1) and SubTask 2 (robot2)
task1_thread = threading.Thread(target=put_watch_in_drawer, args=(robots[0]['name'],))
task2_thread = threading.Thread(target=put_keychain_in_drawer, args=(robots[1]['name'],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put the watch and Keychain inside the drawer is done

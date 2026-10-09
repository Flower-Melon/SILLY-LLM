import threading

# Task Description: Put the watch and Keychain inside the drawer

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Put the Watch inside the Drawer. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# SubTask 2: Put the KeyChain inside the Drawer. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

def put_watch_in_drawer():
    # 0: SubTask 1: Put the Watch inside the Drawer
    # 1: Go to the Watch.
    GoToObject('Watch')
    # 2: Pick up the Watch.
    PickupObject('Watch')
    # 3: Go to the Drawer.
    GoToObject('Drawer')
    # 4: Open the Drawer.
    OpenObject('Drawer')
    # 5: Put the Watch inside the Drawer.
    PutObject('Watch', 'Drawer')
    # 6: Close the Drawer.
    CloseObject('Drawer')

def put_keychain_in_drawer():
    # 0: SubTask 2: Put the KeyChain inside the Drawer
    # 1: Go to the KeyChain.
    GoToObject('KeyChain')
    # 2: Pick up the KeyChain.
    PickupObject('KeyChain')
    # 3: Go to the Drawer.
    GoToObject('Drawer')
    # 4: Open the Drawer.
    OpenObject('Drawer')
    # 5: Put the KeyChain inside the Drawer.
    PutObject('KeyChain', 'Drawer')
    # 6: Close the Drawer.
    CloseObject('Drawer')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_watch_in_drawer)
task2_thread = threading.Thread(target=put_keychain_in_drawer)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put the watch and Keychain inside the drawer is done

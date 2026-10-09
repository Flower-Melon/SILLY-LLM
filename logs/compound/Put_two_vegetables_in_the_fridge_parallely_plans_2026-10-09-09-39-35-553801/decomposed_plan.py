import threading

# Task: Put two vegetables in the fridge in parallel.
# Available vegetables in the scene: Lettuce, Tomato, Potato.
# We choose Lettuce and Tomato as the two vegetables.
# Each subtask is independent, so they can run in parallel.

def put_lettuce_in_fridge():
    # SubTask 1: Put the Lettuce in the Fridge
    GoToObject('Lettuce')          # go to the lettuce
    PickupObject('Lettuce')        # pick it up
    GoToObject('Fridge')           # go to the fridge
    OpenObject('Fridge')           # open the fridge
    PutObject('Lettuce', 'Fridge') # place lettuce inside
    CloseObject('Fridge')          # close the fridge

def put_tomato_in_fridge():
    # SubTask 2: Put the Tomato in the Fridge
    GoToObject('Tomato')           # go to the tomato
    PickupObject('Tomato')         # pick it up
    GoToObject('Fridge')           # go to the fridge
    OpenObject('Fridge')           # open the fridge
    PutObject('Tomato', 'Fridge')  # place tomato inside
    CloseObject('Fridge')          # close the fridge

# Create threads for the two independent subtasks
lettuce_thread = threading.Thread(target=put_lettuce_in_fridge)
tomato_thread = threading.Thread(target=put_tomato_in_fridge)

# Start both subtasks in parallel
lettuce_thread.start()
tomato_thread.start()

# Wait for both subtasks to finish
lettuce_thread.join()
tomato_thread.join()

# Task "Put two vegetables in the fridge parallely" is done

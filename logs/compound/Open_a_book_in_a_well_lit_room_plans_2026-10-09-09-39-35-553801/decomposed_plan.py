# Task Description: Open a book in a well lit room

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Turn on the light in the room. (Skills Required: GoToObject, SwitchOn)
# SubTask 2: Open the book. (Skills Required: GoToObject, OpenObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# CODE
def turn_on_light():
    # 0: SubTask 1: Turn on the light in the room
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch on the LightSwitch to light the room.
    SwitchOn('LightSwitch')

def open_book():
    # 0: SubTask 2: Open the book
    # 1: Go to the Book.
    GoToObject('Book')
    # 2: Open the Book.
    OpenObject('Book')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=turn_on_light)
task2_thread = threading.Thread(target=open_book)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Open a book in a well lit room is done

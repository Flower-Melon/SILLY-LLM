import time
import threading

# Task Description: Break a vase and Turn on TV
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Break a Vase. (Skills Required: GoToObject, BreakObject)
# SubTask 2: Turn on the TV. (Skills Required: GoToObject, SwitchOn)
# These subtasks are independent and can be parallelized.

def break_vase():
    # 0: SubTask 1: Break a Vase
    # 1: Go to the Vase.
    GoToObject('Vase')
    # 2: Break the Vase.
    BreakObject('Vase')

def turn_on_tv():
    # 0: SubTask 2: Turn on the TV
    # 1: Go to the Television.
    GoToObject('Television')
    # 2: Switch on the Television.
    SwitchOn('Television')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=break_vase)
task2_thread = threading.Thread(target=turn_on_tv)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Break a vase and Turn on TV is done

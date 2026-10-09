import time
import threading

# Task Description: Toast a slice of the breadloaf

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Slice the Bread. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
# SubTask 2: Toast the Bread slice. (Skills Required: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff)
# We can execute SubTask 1 first and then SubTask 2, since they cannot be parallelized.

# CODE
def slice_bread():
    # 0: SubTask 1: Slice the Bread
    # 1: Go to the Knife.
    GoToObject('Knife')
    # 2: Pick up the Knife.
    PickupObject('Knife')
    # 3: Go to the Bread.
    GoToObject('Bread')
    # 4: Slice the Bread.
    SliceObject('Bread')
    # 5: Go to the CounterTop.
    GoToObject('CounterTop')
    # 6: Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

def toast_bread():
    # 0: SubTask 2: Toast the Bread slice
    # 1: Go to the sliced Bread.
    GoToObject('Bread')
    # 2: Pick up the sliced Bread.
    PickupObject('Bread')
    # 3: Go to the Toaster.
    GoToObject('Toaster')
    # 4: Put the sliced Bread in the Toaster.
    PutObject('Bread', 'Toaster')
    # 5: Switch on the Toaster.
    SwitchOn('Toaster')
    # 6: Wait for a while to let the Bread toast.
    time.sleep(5)
    # 7: Switch off the Toaster.
    SwitchOff('Toaster')
    # 8: Go to the Bread.
    GoToObject('Bread')
    # 9: Pick up the toasted Bread.
    PickupObject('Bread')
    # 10: Go to the Plate.
    GoToObject('Plate')
    # 11: Put the toasted Bread on the Plate.
    PutObject('Bread', 'Plate')

# Execute SubTask 1
slice_bread()

# Execute SubTask 2
toast_bread()

# Task toast a slice of the breadloaf is done

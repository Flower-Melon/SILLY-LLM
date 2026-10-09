import threading

# Task Description: Slice apple and throw it in the trash
# Decompose into sequential subtasks:
# SubTask 1: Slice the Apple. (Skills Required: GoToObject, PickupObject, SliceObject, PutObject)
# SubTask 2: Throw the Apple slices in the trash. (Skills Required: GoToObject, PickupObject, ThrowObject)
# These subtasks are dependent, so execute sequentially.

def slice_apple():
    # 0: SubTask 1: Slice the Apple
    # 1: Go to the Knife.
    GoToObject('Knife')
    # 2: Pick up the Knife.
    PickupObject('Knife')
    # 3: Go to the Apple.
    GoToObject('Apple')
    # 4: Slice the Apple.
    SliceObject('Apple')
    # 5: Go to the CounterTop.
    GoToObject('CounterTop')
    # 6: Put the Knife back on the CounterTop.
    PutObject('Knife', 'CounterTop')

def throw_apple_in_trash():
    # 0: SubTask 2: Throw the Apple slices in the trash
    # 1: Go to the sliced Apple.
    GoToObject('Apple')
    # 2: Pick up the Apple slices.
    PickupObject('Apple')
    # 3: Go to the GarbageCan.
    GoToObject('GarbageCan')
    # 4: Throw the Apple slices into the trash.
    ThrowObject('Apple', 'GarbageCan')

# Execute SubTask 1
slice_apple()

# Execute SubTask 2
throw_apple_in_trash()

# Task slice apple and throw it in the trash is done

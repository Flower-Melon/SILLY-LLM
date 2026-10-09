import time
import threading

# Task Description: Chill the apple and wash the knife
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Chill the apple. (Skills Required: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# SubTask 2: Wash the knife. (Skills Required: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# TASK ALLOCATION
# Both robots share the same skill set and mass capacity (100), so allocation is driven by
# parallelization and minimum robot count. No skill gaps, no mass gaps -> no teams required.
# Assign robot1 -> SubTask 1 (Chill the apple), robot2 -> SubTask 2 (Wash the knife), run in parallel.

def chill_apple(robot):
    # 0: SubTask 1: Chill the apple
    # 1: Go to the Apple.
    GoToObject(robot, 'Apple')
    # 2: Pick up the Apple.
    PickupObject(robot, 'Apple')
    # 3: Go to the Fridge.
    GoToObject(robot, 'Fridge')
    # 4: Open the Fridge.
    OpenObject(robot, 'Fridge')
    # 5: Put the Apple inside the Fridge to chill.
    PutObject(robot, 'Apple', 'Fridge')
    # 6: Close the Fridge.
    CloseObject(robot, 'Fridge')

def wash_knife(robot):
    # 0: SubTask 2: Wash the knife
    # 1: Go to the Knife.
    GoToObject(robot, 'Knife')
    # 2: Pick up the Knife.
    PickupObject(robot, 'Knife')
    # 3: Go to the Sink.
    GoToObject(robot, 'Sink')
    # 4: Put the Knife inside the Sink.
    PutObject(robot, 'Knife', 'Sink')
    # 5: Switch on the Faucet to wash the Knife.
    SwitchOn(robot, 'Faucet')
    # 6: Wait for a while to let the Knife wash.
    time.sleep(5)
    # 7: Switch off the Faucet.
    SwitchOff(robot, 'Faucet')
    # 8: Pick up the clean Knife.
    PickupObject(robot, 'Knife')
    # 9: Go to the CounterTop.
    GoToObject(robot, 'CounterTop')
    # 10: Place the Knife on the CounterTop.
    PutObject(robot, 'Knife', 'CounterTop')

# Parallelize SubTask 1 (robot1) and SubTask 2 (robot2)
task1_thread = threading.Thread(target=chill_apple, args=(robots[0]['name'],))
task2_thread = threading.Thread(target=wash_knife, args=(robots[1]['name'],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Chill the apple and wash the knife is done

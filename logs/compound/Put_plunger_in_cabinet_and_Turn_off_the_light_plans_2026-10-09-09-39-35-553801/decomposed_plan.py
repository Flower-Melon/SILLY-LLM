import threading

# Task Description: Put plunger in cabinet and Turn off the light.
# Decompose into independent subtasks that can be parallelized:
# SubTask 1: Put the Plunger in the Cabinet. (Skills: GoToObject, PickupObject, OpenObject, PutObject, CloseObject)
# SubTask 2: Turn off the Light. (Skills: GoToObject, SwitchOff)
# These subtasks are independent, so run them in parallel.

def put_plunger_in_cabinet():
    # 0: SubTask 1: Put the Plunger in the Cabinet
    # 1: Go to the Plunger.
    GoToObject('Plunger')
    # 2: Pick up the Plunger.
    PickupObject('Plunger')
    # 3: Go to the Cabinet.
    GoToObject('Cabinet')
    # 4: Open the Cabinet.
    OpenObject('Cabinet')
    # 5: Put the Plunger inside the Cabinet.
    PutObject('Plunger', 'Cabinet')
    # 6: Close the Cabinet.
    CloseObject('Cabinet')

def turn_off_light():
    # 0: SubTask 2: Turn off the Light
    # 1: Go to the LightSwitch.
    GoToObject('LightSwitch')
    # 2: Switch off the LightSwitch.
    SwitchOff('LightSwitch')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=put_plunger_in_cabinet)
task2_thread = threading.Thread(target=turn_off_light)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Put plunger in cabinet and Turn off the light is done

import time
import threading

# Task Description: Open a book in a well lit room
# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Turn on the light in the room. (Skills Required: GoToObject, SwitchOn)
# SubTask 2: Open the book. (Skills Required: GoToObject, OpenObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'BreakObject', 'ThrowObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'OpenObject', 'CloseObject'], 'mass_capacity': 100}, {'name': 'robot3', 'skills': ['GoToObject', 'SwitchOn', 'SwitchOff'], 'mass_capacity': 100}]
# SOLUTION
# All the robots DONOT share the same set and number of skills (no_skills) & all objects have different masses. In this case where all robots have different sets of skills and objects have different mass - Focus on Task Allocation based on Robot Skills alone.
# Analyze the skills required for each subtask and the skills each robot possesses. In this scenario, we have two main subtasks: 'Turn on the light in the room' and 'Open the book'.
# For the 'Turn on the light in the room' subtask, it requires 'GoToObject' and 'SwitchOn' skills. In this case, Robot 3 has both these skills.
# For the 'Open the book' subtask, it requires 'GoToObject' and 'OpenObject' skills. In this case, Robot 2 has both these skills.
# No teams are required since SubTasks can be performed with individual robots as explained above. The 'Turn on the light in the room' subtask is assigned to Robot 3. The 'Open the book' subtask is assigned to Robot 2.
# The two subtasks are independent and assigned to different robots, so they can be executed in parallel.

# Code Solution
def turn_on_light(robot_list):
    # robot_list = [robot3]
    # 0: SubTask 1: Turn on the light in the room
    # 1: Go to the LightSwitch using robot3.
    GoToObject(robot_list[0], 'LightSwitch')
    # 2: Switch on the LightSwitch to light the room using robot3.
    SwitchOn(robot_list[0], 'LightSwitch')

def open_book(robot_list):
    # robot_list = [robot2]
    # 0: SubTask 2: Open the book
    # 1: Go to the Book using robot2.
    GoToObject(robot_list[0], 'Book')
    # 2: Open the Book using robot2.
    OpenObject(robot_list[0], 'Book')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=turn_on_light, args=([robots[2]],))
task2_thread = threading.Thread(target=open_book, args=([robots[1]],))

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Open a book in a well lit room is done

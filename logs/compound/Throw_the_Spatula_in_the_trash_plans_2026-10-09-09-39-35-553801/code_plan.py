import time
import threading

# Task Description: Throw the Spatula in the trash

# GENERAL TASK DECOMPOSITION
# Independent subtasks:
# SubTask 1: Throw the Spatula in the trash. (Skills Required: GoToObject, PickupObject, ThrowObject)
# We can execute SubTask 1.

# TASK ALLOCATION
robots = [{'name': 'robot1', 'skills': ['GoToObject', 'BreakObject', 'ThrowObject'], 'mass_capacity': 100}, {'name': 'robot2', 'skills': ['GoToObject', 'PickupObject', 'PutObject'], 'mass_capacity': 100}]
# SOLUTION
# All the robots DONOT share the same set and number of skills (no_skills) & all objects have different masses. In this case where all robots have different sets of skills and objects have different mass - Focus on Task Allocation based on Robot Skills alone.
# Analyze the skills required for each subtask and the skills each robot possesses. In this scenario, we have one main subtask: 'Throw the Spatula in the trash'.
# For the 'Throw the Spatula in the trash' subtask, it requires 'GoToObject', 'PickupObject', and 'ThrowObject' skills. However, no individual robot has all these skills. This is a skill gap that needs to be addressed. Form a team of robots. The skills of the team must be 'GoToObject', 'PickupObject', and 'ThrowObject'. Team of Robots 1 and 2 have all the skills required where robot1 has the 'GoToObject' and 'ThrowObject' skills and robot2 has the 'GoToObject' and 'PickupObject' skills.
# Teams are required since SubTasks can't be performed with individual robots as explained above. The 'Throw the Spatula in the trash' subtask is assigned to team of Robots 1 and 2.

# Code Solution
def throw_spatula_in_trash(robot_list):
    # robot_list = [robot1, robot2]
    # 0: SubTask 1: Throw the Spatula in the trash
    # 1: Go to the Spatula using robot2.
    GoToObject(robot_list[1], 'Spatula')
    # 2: Pick up the Spatula using robot2.
    PickupObject(robot_list[1], 'Spatula')
    # 3: Go to the GarbageCan using robot1.
    GoToObject(robot_list[0], 'GarbageCan')
    # 4: Throw the Spatula into the GarbageCan using robot1.
    ThrowObject(robot_list[0], 'Spatula', 'GarbageCan')

# Perform SubTask 1 with team of robot1 and robot2
task1_thread = threading.Thread(target=throw_spatula_in_trash, args=([robots[0], robots[1]],))
# Start executing SubTask 1
task1_thread.start()
# Join the task thread before finishing
task1_thread.join()
# Task Throw the Spatula in the trash is done

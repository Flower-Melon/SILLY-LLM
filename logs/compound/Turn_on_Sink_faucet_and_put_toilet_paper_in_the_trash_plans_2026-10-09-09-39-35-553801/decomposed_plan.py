# Task Description: Turn on Sink faucet and put toilet paper in the trash

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Turn on the Sink faucet. (Skills Required: GoToObject, SwitchOn)
# SubTask 2: Put toilet paper in the trash. (Skills Required: GoToObject, PickupObject, PutObject)
# We can parallelize SubTask 1 and SubTask 2 because they don't depend on each other.

# CODE
def turn_on_sink_faucet():
    # 0: SubTask 1: Turn on the Sink faucet
    # 1: Go to the Sink.
    GoToObject('Sink')
    # 2: Switch on the Faucet.
    SwitchOn('Faucet')

def put_toilet_paper_in_trash():
    # 0: SubTask 2: Put toilet paper in the trash
    # 1: Go to the ToiletPaper.
    GoToObject('ToiletPaper')
    # 2: Pick up the ToiletPaper.
    PickupObject('ToiletPaper')
    # 3: Go to the GarbageCan.
    GoToObject('GarbageCan')
    # 4: Put the ToiletPaper in the GarbageCan.
    PutObject('ToiletPaper', 'GarbageCan')

# Parallelize SubTask 1 and SubTask 2
task1_thread = threading.Thread(target=turn_on_sink_faucet)
task2_thread = threading.Thread(target=put_toilet_paper_in_trash)

# Start executing SubTask 1 and SubTask 2 in parallel
task1_thread.start()
task2_thread.start()

# Wait for both SubTask 1 and SubTask 2 to finish
task1_thread.join()
task2_thread.join()

# Task Turn on Sink faucet and put toilet paper in the trash is done

# Task Description: Wash the fork and put it in the bowl

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Wash the Fork. (Skills Required: GoToObject, PickupObject, PutObject, SwitchOn, SwitchOff)
# SubTask 2: Put the Fork in the Bowl. (Skills Required: GoToObject, PickupObject, PutObject)
# We cannot parallelize these subtasks because SubTask 2 depends on SubTask 1 (the fork must be washed before placing it in the bowl).

# CODE
def wash_fork():
    # 0: SubTask 1: Wash the Fork
    # 1: Go to the Fork.
    GoToObject('Fork')
    # 2: Pick up the Fork.
    PickupObject('Fork')
    # 3: Go to the Sink.
    GoToObject('Sink')
    # 4: Put the Fork inside the Sink.
    PutObject('Fork', 'Sink')
    # 5: Switch on the Faucet to clean the Fork.
    SwitchOn('Faucet')
    # 6: Wait for a while to let the Fork clean.
    time.sleep(5)
    # 7: Switch off the Faucet.
    SwitchOff('Faucet')
    # 8: Pick up the clean Fork.
    PickupObject('Fork')

def put_fork_in_bowl():
    # 0: SubTask 2: Put the Fork in the Bowl
    # 1: Go to the Bowl.
    GoToObject('Bowl')
    # 2: Put the Fork inside the Bowl.
    PutObject('Fork', 'Bowl')

# Execute SubTask 1
wash_fork()

# Execute SubTask 2 after SubTask 1 is complete
put_fork_in_bowl()

# Task Wash the fork and put it in the bowl is done

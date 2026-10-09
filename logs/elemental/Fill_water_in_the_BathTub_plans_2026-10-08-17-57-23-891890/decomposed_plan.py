# Task Description: Fill water in the BathTub

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Fill water in the BathTub. (Skills Required: GoToObject, SwitchOn, SwitchOff)
# We can execute SubTask 1.

# CODE
def fill_bathtub():
    # 0: SubTask 1: Fill water in the BathTub
    # 1: Go to the Bathtub.
    GoToObject('Bathtub')
    # 2: Switch on the Faucet to fill the Bathtub with water.
    SwitchOn('Faucet')
    # 3: Wait for a while to let the Bathtub fill with water.
    time.sleep(5)
    # 4: Switch off the Faucet.
    SwitchOff('Faucet')

# Execute SubTask 1
fill_bathtub()

# Task Fill water in the BathTub is done

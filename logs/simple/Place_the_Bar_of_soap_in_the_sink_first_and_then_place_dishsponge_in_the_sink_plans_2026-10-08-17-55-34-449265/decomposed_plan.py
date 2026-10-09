import threading

# Task Description: Place the Bar of soap in the sink first and then place dishsponge in the sink

# GENERAL TASK DECOMPOSITION
# Decompose and parallelize subtasks where ever possible
# Independent subtasks:
# SubTask 1: Place the Bar of soap in the sink. (Skills Required: GoToObject, PickupObject, PutObject)
# SubTask 2: Place the dishsponge in the sink. (Skills Required: GoToObject, PickupObject, PutObject)
# We cannot parallelize SubTask 1 and SubTask 2 because the task requires the soap to be placed first.

# CODE
def place_soap_in_sink():
    # 0: SubTask 1: Place the Bar of soap in the sink
    # 1: Go to the SoapBar.
    GoToObject('SoapBar')
    # 2: Pick up the SoapBar.
    PickupObject('SoapBar')
    # 3: Go to the Sink.
    GoToObject('Sink')
    # 4: Put the SoapBar in the Sink.
    PutObject('SoapBar', 'Sink')

def place_dishsponge_in_sink():
    # 0: SubTask 2: Place the dishsponge in the sink
    # 1: Go to the DishSponge.
    GoToObject('DishSponge')
    # 2: Pick up the DishSponge.
    PickupObject('DishSponge')
    # 3: Go to the Sink.
    GoToObject('Sink')
    # 4: Put the DishSponge in the Sink.
    PutObject('DishSponge', 'Sink')

# Execute SubTask 1 first
place_soap_in_sink()

# Execute SubTask 2 after SubTask 1 is complete
place_dishsponge_in_sink()

# Task Place the Bar of soap in the sink first and then place dishsponge in the sink is done

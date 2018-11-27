
import random

class PriorityRandom:

    def __init__(self):
        pass

    def apply(self, firedex_configuration, network_flows):
        priorities = range( 1, 1 + firedex_configuration.priorities() )

        for network_flow in network_flows:
            priority = random.sample(population = priorities, k = 1)[0]
            network_flow.set_priority(priority = priority)

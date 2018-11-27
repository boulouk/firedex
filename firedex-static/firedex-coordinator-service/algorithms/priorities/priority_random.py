
import random

class PriorityRandom:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, experiment_configuration, network_flows):
        priorities = range(1, 1 + firedex_configuration["priorities"])

        for network_flow in network_flows:
            priority = random.sample(priorities, 1)[0]
            network_flow["priority"] = priority

        return network_flows


import json
from scenario.firedex_scenario import *

class FiredexConfiguration:

    def __init__(self):
        self.__network_flows = NETWORK_FLOWS
        self.__priorities = PRIORITIES

        self.__network_flow_algorithm = NETWORK_FLOW_ALGORITHM
        self.__priority_algorithm = PRIORITY_ALGORITHM
        self.__drop_rate_algorithm = DROP_RATE_ALGORITHM

        self.__rho_tolerance = RHO_TOLERANCE

    def network_flows(self):
        return self.__network_flows

    def priorities(self):
        return self.__priorities

    def network_flow_algorithm(self):
        return self.__network_flow_algorithm

    def priority_algorithm(self):
        return self.__priority_algorithm

    def drop_rate_algorithm(self):
        return self.__drop_rate_algorithm

    def rho_tolerance(self):
        return self.__rho_tolerance

    def as_dictionary(self):
        object = {
            "network_flows": self.network_flows(),
            "priorities": self.priorities(),

            "network_flow_algorithm": self.network_flow_algorithm(),
            "priority_algorithm": self.priority_algorithm(),
            "drop_rate_algorithm": self.drop_rate_algorithm(),

            "rho_tolerance": self.rho_tolerance()
        }

        return object

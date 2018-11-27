
import json
from scenario.firedex_scenario import *

class FiredexConfiguration:

    def __init__(self):
        self.__host = HOST
        self.__port = PORT

        self.__experiment_duration = EXPERIMENT_DURATION

        self.__network_flows = NETWORK_FLOWS
        self.__priorities = PRIORITIES

        self.__network_flow_algorithm = NETWORK_FLOW_ALGORITHM
        self.__priority_algorithm = PRIORITY_ALGORITHM
        self.__drop_rate_algorithm = DROP_RATE_ALGORITHM

        self.__tolerance = TOLERANCE

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def experiment_duration(self):
        return self.__experiment_duration

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

    def tolerance(self):
        return self.__tolerance

    def json(self):
        object = {
            "host": self.host(),
            "port": self.port(),

            "experiment_duration": self.experiment_duration(),

            "network_flows": self.network_flows(),
            "priorities": self.priorities(),

            "network_flow_algorithm": self.network_flow_algorithm(),
            "priority_algorithm": self.priority_algorithm(),
            "drop_rate_algorithm": self.drop_rate_algorithm(),

            "tolerance": self.tolerance()
        }

        result = json.dumps(object, indent = 4, sort_keys = False)
        return result

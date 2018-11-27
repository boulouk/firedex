
import json
from scenario.network_scenario import *

class NetworkConfiguration:

    def __init__(self):
        self.__bandwidth = BANDWIDTH
        self.__latency = LATENCY
        self.__error_rate = ERROR_RATE

    def bandwidth(self):
        return self.__bandwidth

    def latency(self):
        return self.__latency

    def error_rate(self):
        return self.__error_rate

    def json(self):
        object = {
            "bandwidth": self.bandwidth(),
            "latency": self.latency(),
            "error_rate": self.error_rate()
        }

        result = json.dumps(object, indent = 4, sort_keys = False)
        return result

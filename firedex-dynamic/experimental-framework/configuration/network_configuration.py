
import json
from scenario.network_scenario import *

class NetworkConfiguration:

    def __init__(self):
        self.__bandwidth = BANDWIDTH
        self.__delay = DELAY
        self.__error_rate = ERROR_RATE

    def bandwidth(self):
        return self.__bandwidth

    def delay(self):
        return self.__delay

    def error_rate(self):
        return self.__error_rate

    def as_dictionary(self):
        object = {
            "bandwidth": self.bandwidth(),
            "delay": self.delay(),
            "error_rate": self.error_rate()
        }

        return object

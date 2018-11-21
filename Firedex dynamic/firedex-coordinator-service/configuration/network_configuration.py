
class NetworkConfiguration:

    def __init__(self, bandwidth, delay, error_rate):
        self.__bandwidth = bandwidth
        self.__delay = delay
        self.__error_rate = error_rate

    def bandwidth(self):
        return self.__bandwidth

    def delay(self):
        return self.__delay

    def error_rate(self):
        return self.__error_rate

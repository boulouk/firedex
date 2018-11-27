
from scenario.controller_scenario import *

class ControllerConfiguration:

    def __init__(self):
        self.__host = HOST
        self.__port = PORT

        self.__switch_identifier = SWITCH_IDENTIFIER

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def switch_identifier(self):
        return self.__switch_identifier

    def as_dictionary(self):
        object = {
            "host": self.host(),
            "port": self.port(),

            "switch_identifier": self.switch_identifier()
        }

        return object

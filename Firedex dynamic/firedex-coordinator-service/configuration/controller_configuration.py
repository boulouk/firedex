
class ControllerConfiguration:

    def __init__(self, host, port, switch_identifier):
        self.__host = host
        self.__port = port
        self.__switch_identifier = switch_identifier

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def switch_identifier(self):
        return self.__switch_identifier


UDP_OVERHEAD = 42
MQTT_SN_OVERHEAD = 7

class Publication:

    def __init__(self, publisher, topic, rate, message_size):
        self.__publisher = publisher
        self.__topic = topic
        self.__rate = rate
        self.__message_size = message_size

    def publisher(self):
        return self.__publisher

    def topic(self):
        return self.__topic

    def rate(self):
        return self.__rate

    def message_size(self):
        return self.__message_size

    def publication_load(self):
        publication_load = self.rate() * ( self.message_size() + UDP_OVERHEAD + MQTT_SN_OVERHEAD )
        return publication_load

    def __eq__(self, that):
        equals = True
        equals = equals and self.publisher() == that.publisher()
        equals = equals and self.topic() == that.topic()
        return equals

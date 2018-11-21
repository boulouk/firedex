
import json
from scenario.topology_scenario import *

class TopologyConfiguration:

    def __init__(self):
        self.__broker = BROKER

        self.__types = TYPES

        self.__topics = TOPICS
        self.__topic = TOPIC

        self.__subscribers = SUBSCRIBERS
        self.__subscriber = SUBSCRIBER

        self.__publishers = PUBLISHERS
        self.__publisher = PUBLISHER

    def broker(self):
        return self.__broker

    def types(self):
        return self.__types

    def topics(self):
        return self.__topics

    def topic(self):
        return self.__topic

    def subscribers(self):
        return self.__subscribers

    def subscriber(self):
        return self.__subscriber

    def publishers(self):
        return self.__publishers

    def publisher(self):
        return self.__publisher

    def json(self):
        object = {
            "broker": self.broker(),

            "classes": self.types(),

            "topics": self.topics(),
            "topic": self.topic(),

            "subscribers": self.subscribers(),
            "subscriber": self.subscriber(),

            "publishers": self.publishers(),
            "publisher": self.publisher()
        }

        result = json.dumps(object, indent = 4, sort_keys = False)
        return result

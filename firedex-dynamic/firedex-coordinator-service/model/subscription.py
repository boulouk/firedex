
class Subscription:

    def __init__(self, subscriber, topic, utility_function, adjusted_utility_function):
        self.__subscriber = subscriber
        self.__topic = topic
        self.__utility_function = utility_function
        self.__adjusted_utility_function = adjusted_utility_function

    def subscriber(self):
        return self.__subscriber

    def topic(self):
        return self.__topic

    def utility_function(self):
        return self.__utility_function

    def adjusted_utility_function(self):
        return self.__adjusted_utility_function

    def __eq__(self, that):
        equals = True
        equals = equals and self.subscriber() == that.subscriber()
        equals = equals and self.topic() == that.topic()
        return equals

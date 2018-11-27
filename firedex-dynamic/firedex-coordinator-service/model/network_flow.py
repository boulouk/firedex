
from model.subscription import Subscription

class NetworkFlow:

    def __init__(self, subscriber, host, port):
        self.__subscriber = subscriber
        self.__host = host
        self.__port = port

        self.__subscriptions = []

        self.__priority = None
        self.__drop_rate = None

    def subscriber(self):
        return self.__subscriber

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def subscriptions(self):
        return self.__subscriptions

    def add_subscription(self, topic, utility_function, adjusted_utility_function):
        subscription = Subscription(
            subscriber = self.subscriber(),
            topic = topic,
            utility_function = utility_function,
            adjusted_utility_function = adjusted_utility_function
        )

        self.subscriptions().append(subscription)

    def remove_subscription(self, topic):
        dummy_utility_function = -1
        dummy_adjusted_utility_function = -1

        subscription = Subscription(
            subscriber = self.subscriber(),
            topic = topic,
            utility_function = dummy_utility_function,
            adjusted_utility_function = dummy_adjusted_utility_function
        )

        self.subscriptions().remove(subscription)

    def utility_function(self):
        utility_function = 0

        for subscription in self.subscriptions():
            utility_function = utility_function + subscription.utility_function()

        return utility_function

    def adjusted_utility_function(self):
        adjusted_utility_function = 0

        for subscription in self.subscriptions():
            adjusted_utility_function = adjusted_utility_function + subscription.adjusted_utility_function()

        return adjusted_utility_function

    def get_priority(self):
        return self.__priority

    def set_priority(self, priority):
        self.__priority = priority

    def get_drop_rate(self):
        return self.__drop_rate

    def set_drop_rate(self, drop_rate):
        self.__drop_rate = drop_rate

    def __eq__(self, that):
        equals = True
        equals = equals and self.subscriber() == that.subscriber()
        equals = equals and self.host() == that.host()
        equals = equals and self.port() == that.port()
        return equals

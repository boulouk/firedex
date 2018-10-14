
UDP_OVERHEAD = 42
MQTT_SN_OVERHEAD = 7

class DropRateLinear:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, experiment_configuration, network_flows):
        bandwidth = network_configuration["bandwidth"]
        tolerance = firedex_configuration["tolerance"]

        network_load_by_topic = {}

        publishers = experiment_configuration["publishers"]
        for publisher in publishers:
            publisher = publisher["publisher"]
            publications = publisher["publications"]

            for publication in publications:
                topic = publication["topic"]

                if topic not in network_load_by_topic:
                    network_load_by_topic[topic] = 0

                rate = publication["rate"]
                message_size = publication["messageSize"] + UDP_OVERHEAD + MQTT_SN_OVERHEAD

                publication_network_load = rate * message_size
                network_load_by_topic[topic] = network_load_by_topic[topic] + publication_network_load

        network_load = 0
        network_load_with_priority = 0

        subscribers = experiment_configuration["subscribers"]
        for subscriber in subscribers:
            subscriber = subscriber["subscriber"]

            identifier = subscriber["identifier"]
            subscriptions = subscriber["subscriptions"]
            for subscription in subscriptions:
                topic = subscription["topic"]

                if topic not in network_load_by_topic:
                    subscription_network_load = 0
                else:
                    subscription_network_load = network_load_by_topic[topic]

                network_load = network_load + subscription_network_load

                subscriber_network_flow = self.__subscriber_network_flow(network_flows, identifier, topic)
                priority = subscriber_network_flow["priority"]
                network_load_with_priority = network_load_with_priority + ( subscription_network_load * (priority - 1) )

        if network_load <= ( bandwidth * (1 - tolerance) ):
            beta = 0
        else:
            beta = (- bandwidth * (1 - tolerance) + network_load) / network_load_with_priority

        for network_flow in network_flows:
            priority = network_flow["priority"]
            priority = priority - 1
            drop_rate = beta * priority
            if drop_rate > 1:
                drop_rate = 1

            network_flow["drop_rate"] = drop_rate

        return network_flows

    def __subscriber_network_flow(self, network_flows, identifier, topic):
        for network_flow in network_flows:
            subscriber_identifier = network_flow["identifier"]
            subscriber_subscriptions = network_flow["subscriptions"]
            if subscriber_identifier == identifier and self.__exists_subscription(subscriber_subscriptions, topic):
                return network_flow

        return None

    def __exists_subscription(self, subscriptions, topic):
        for subscription in subscriptions:
            subscription_topic = subscription["topic"]
            if subscription_topic == topic:
                return True

        return False

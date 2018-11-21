
UDP_OVERHEAD = 42
MQTT_SN_OVERHEAD = 7

class DropRateFlat:

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

        subscribers = experiment_configuration["subscribers"]
        for subscriber in subscribers:
            subscriber = subscriber["subscriber"]
            subscriptions = subscriber["subscriptions"]
            for subscription in subscriptions:
                topic = subscription["topic"]

                if topic not in network_load_by_topic:
                    subscription_network_load = 0
                else:
                    subscription_network_load = network_load_by_topic[topic]

                network_load = network_load + subscription_network_load

        if network_load <= ( bandwidth * (1 - tolerance) ):
            beta = 0
        else:
            beta = - ( bandwidth * (1 - tolerance) ) / network_load + 1

        for network_flow in network_flows:
            drop_rate = beta
            network_flow["drop_rate"] = drop_rate

        return network_flows


import numpy

UDP_OVERHEAD = 42
MQTT_SN_OVERHEAD = 7

class DropRateExponential:

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

        priorities = range(1, 1 + firedex_configuration["priorities"])

        network_flows_by_priority = self.__network_flows_by_priority(priorities, network_flows)

        tot = 0
        coefficients = []
        for priority, network_flows_with_priority in sorted(network_flows_by_priority.iteritems(), reverse = True):
            coefficient = 0
            for network_flow_with_priority in network_flows_with_priority:
                network_flow_subscriptions = network_flow_with_priority["subscriptions"]
                for network_flow_subscription in network_flow_subscriptions:
                    topic = network_flow_subscription["topic"]

                    if topic not in network_load_by_topic:
                        topic_network_load = 0
                    else:
                        topic_network_load = network_load_by_topic[topic]

                    coefficient = coefficient + topic_network_load

                    tot = tot + topic_network_load

            coefficients.append(coefficient)

        coefficients[-1] = coefficients[-1] - (bandwidth * (1 - tolerance))

        roots = numpy.roots(coefficients)

        true_roots = []
        for root in roots:
            if numpy.isreal(root) and 0 < root <= 1:
                true_roots.append(abs(root))

        if true_roots.__len__() == 0:
            true_roots.append(1)

        alpha = numpy.amax(true_roots)
        beta = 1 / alpha

        for network_flow in network_flows:
            priority = network_flow["priority"]
            priority = priority - 1
            drop_rate = 1 - (float(beta) ** (- priority))
            network_flow["drop_rate"] = drop_rate

        return network_flows

    def __network_flows_by_priority(self, priorities, network_flows):
        network_flows_by_priority = {}

        for priority in priorities:
            network_flows_by_priority[priority] = []

            for network_flow in network_flows:
                network_flow_priority = network_flow["priority"]
                if network_flow_priority == priority:
                    network_flows_by_priority[priority].append(network_flow)

        return network_flows_by_priority


import numpy

class DropRateExponential:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, publishers_configuration, network_flows):
        bandwidth = network_configuration.bandwidth()
        priorities = range( 1, 1 + firedex_configuration.priorities() )
        rho_tolerance = firedex_configuration.rho_tolerance()
        publication_collection = publishers_configuration.publication_collection()

        network_flows_by_priority = self.__network_flows_by_priority(
            priorities = priorities,
            network_flows = network_flows
        )

        network_flows_load = 0
        coefficients = []

        for network_flow_priority, network_flows_with_priority in sorted(network_flows_by_priority.iteritems(), reverse = True):
            coefficient = 0
            for network_flow_with_priority in network_flows_with_priority:
                network_flow_subscriptions = network_flow_with_priority.subscriptions()
                for network_flow_subscription in network_flow_subscriptions:
                    subscription_topic = network_flow_subscription.topic()
                    subscription_load = publication_collection.publications_load_by_topic(topic = subscription_topic)

                    network_flows_load += subscription_load
                    coefficient += subscription_load

            coefficients.append(coefficient)

        if network_flows_load <= ( bandwidth * (1 - rho_tolerance) ):
            beta = 1
        else:
            coefficients[-1] = coefficients[-1] - (bandwidth * (1 - rho_tolerance))

            roots = numpy.roots(p = coefficients)

            alpha = None
            for root in roots:
                if numpy.isreal(root) and 0 < root <= 1:
                    alpha = abs(root)

            beta = 1 / alpha

        for network_flow in network_flows:
            network_flow_priority = network_flow.get_priority()
            network_flow_priority = network_flow_priority - 1
            network_flow_drop_rate = 1 - ( float(beta) ** (- network_flow_priority) )
            network_flow_drop_rate = round(network_flow_drop_rate, 2)
            network_flow.set_drop_rate(drop_rate = network_flow_drop_rate)

    def __network_flows_by_priority(self, priorities, network_flows):
        network_flows_by_priority = {}

        for priority in priorities:
            network_flows_by_priority[priority] = []

            for network_flow in network_flows:
                network_flow_priority = network_flow.get_priority()
                if network_flow_priority == priority:
                    network_flows_by_priority[priority].append(network_flow)

        return network_flows_by_priority

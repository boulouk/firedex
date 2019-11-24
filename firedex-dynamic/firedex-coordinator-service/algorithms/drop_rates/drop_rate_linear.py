
class DropRateLinear:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, publishers_configuration, network_flows):
        bandwidth = network_configuration.bandwidth()
        rho_tolerance = firedex_configuration.rho_tolerance()
        publication_collection = publishers_configuration.publication_collection()

        network_flows_load = 0
        network_flows_load_with_priority = 0

        for network_flow in network_flows:
            network_flow_subscriptions = network_flow.subscriptions()
            network_flow_priority = network_flow.get_priority()
            for network_flow_subscription in network_flow_subscriptions:
                subscription_topic = network_flow_subscription.topic()
                subscription_load = publication_collection.publications_load_by_topic(topic = subscription_topic)

                network_flows_load += subscription_load
                network_flows_load_with_priority += ( subscription_load * (network_flow_priority - 1) )

        if network_flows_load <= ( bandwidth * (1 - rho_tolerance) ):
            beta = 0
        else:
            a = - bandwidth * (1 - rho_tolerance)
            b = - bandwidth * (1 - rho_tolerance) + network_flows_load
            c = b / network_flows_load_with_priority
            beta = (- bandwidth * (1 - rho_tolerance) + network_flows_load) / network_flows_load_with_priority

        for network_flow in network_flows:
            network_flow_priority = network_flow.get_priority()
            network_flow_priority = network_flow_priority - 1

            network_flow_drop_rate = beta * network_flow_priority
            # network_flow_drop_rate = round(network_flow_drop_rate, 2)

            if network_flow_drop_rate > 1:
                network_flow_drop_rate = 1

            network_flow.set_drop_rate(drop_rate = network_flow_drop_rate)

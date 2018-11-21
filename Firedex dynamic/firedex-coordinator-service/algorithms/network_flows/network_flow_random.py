
import random
from model.network_flow import NetworkFlow

class NetworkFlowRandom:

    def __init__(self):
        pass

    def apply(self, firedex_configuration, subscriber, host, subscriber_subscriptions):
        network_flows = range( 10001, 10001 + firedex_configuration.network_flows() )

        subscriber_network_flows = []

        for port in network_flows:
            subscriber_network_flow = NetworkFlow(
                subscriber = subscriber,
                host = host,
                port = port
            )
            subscriber_network_flows.append(subscriber_network_flow)

        for subscriber_subscription in subscriber_subscriptions:
            port = random.sample(population = network_flows, k = 1)[0]
            subscriber_network_flow = self.__subscriber_network_flow(
                subscriber_network_flows = subscriber_network_flows,
                port = port
            )

            subscriber_network_flow.add_subscription(
                topic = subscriber_subscription.topic(),
                utility_function = subscriber_subscription.utility_function(),
                adjusted_utility_function = subscriber_subscription.adjusted_utility_function()
            )

        subscriber_network_flows = self.__remove_empty_network_flows(
            subscriber_network_flows = subscriber_network_flows
        )

        return subscriber_network_flows

    def __subscriber_network_flow(self, subscriber_network_flows, port):
        for subscriber_network_flow in subscriber_network_flows:
            subscriber_port = subscriber_network_flow.port()
            if subscriber_port == port:
                return subscriber_network_flow

        # should not reach this line

    def __remove_empty_network_flows(self, subscriber_network_flows):
        new_subscriber_network_flows = []

        for subscriber_network_flow in subscriber_network_flows:
            if subscriber_network_flow.subscriptions():
                new_subscriber_network_flows.append(subscriber_network_flow)

        return new_subscriber_network_flows


from operator import itemgetter
from model.network_flow import NetworkFlow

class NetworkFlowGreedySplit:

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

        subscriber_subscriptions.sort(
            key = lambda x: x.adjusted_utility_function(),
            reverse = True
        )

        grouped_subscriber_subscriptions = self.__even_group_split(
            subscriber_subscriptions = subscriber_subscriptions,
            groups = network_flows.__len__()
        )

        for subscriber_network_flow, subscriber_subscriptions in zip(subscriber_network_flows, grouped_subscriber_subscriptions):
            for subscriber_subscription in subscriber_subscriptions:
                subscriber_network_flow.add_subscription(
                    topic = subscriber_subscription.topic(),
                    utility_function = subscriber_subscription.utility_function(),
                    adjusted_utility_function = subscriber_subscription.adjusted_utility_function()
                )

        subscriber_network_flows = self.__remove_empty_network_flows(
            subscriber_network_flows = subscriber_network_flows
        )

        return subscriber_network_flows

    def __even_group_split(self, subscriber_subscriptions, groups):
        groups_size = []
        base_size = subscriber_subscriptions.__len__() // groups
        surplus = subscriber_subscriptions.__len__() % groups

        for i in range(groups):
            group_size = base_size
            if i < surplus:
                group_size = group_size + 1
            groups_size.append(group_size)

        grouped_subscriptions = []

        index = 0
        for i in range(groups):
            group_size = groups_size[i]
            grouped_subscriptions.append(subscriber_subscriptions[index:index + group_size])
            index = index + group_size

        return grouped_subscriptions

    def __remove_empty_network_flows(self, subscriber_network_flows):
        new_subscriber_network_flows = []

        for subscriber_network_flow in subscriber_network_flows:
            if subscriber_network_flow.subscriptions():
                new_subscriber_network_flows.append(subscriber_network_flow)

        return new_subscriber_network_flows


class PriorityGreedySplitLocal:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, experiment_configuration, network_flows):
        priorities = range(1, 1 + firedex_configuration["priorities"])

        new_network_flows = []

        subscribers = self.__subscribers(network_flows)

        for subscriber in subscribers:
            subscriber_network_flows = self.__network_flows_by_subscriber(subscriber, network_flows)

            subscriber_network_flows = sorted(
                                   subscriber_network_flows,
                                   key = lambda subscriber_network_flow: subscriber_network_flow["network_flow"]["utility_function"],
                                   reverse = True
                                  )

            grouped_network_flows = self.__even_group_split(subscriber_network_flows, priorities.__len__())

            for priority, grouped_network_flows_by_priority in zip(priorities, grouped_network_flows):
                for network_flow_by_priority in grouped_network_flows_by_priority:
                    network_flow_by_priority["priority"] = priority
                    new_network_flows.append(network_flow_by_priority)

        return new_network_flows

    def __subscribers(self, network_flows):
        subscribers = []
        for network_flow in network_flows:
            identifier = network_flow["identifier"]
            if identifier not in subscribers:
                subscribers.append(identifier)

        return subscribers

    def __network_flows_by_subscriber(self, identifier, network_flows):
        subscriber_network_flows = []
        for network_flow in network_flows:
            subscriber_identifier = network_flow["identifier"]
            if subscriber_identifier == identifier:
                subscriber_network_flows.append(network_flow)

        return subscriber_network_flows

    def __even_group_split(self, network_flows, groups):
        groups_size = []
        base_size = network_flows.__len__() // groups
        surplus = network_flows.__len__() % groups

        for i in range(groups):
            group_size = base_size
            if i < surplus:
                group_size = group_size + 1
            groups_size.append(group_size)

        grouped_subscriptions = []

        index = 0
        for i in range(groups):
            group_size = groups_size[i]
            grouped_subscriptions.append(network_flows[index:index + group_size])
            index = index + group_size

        return grouped_subscriptions

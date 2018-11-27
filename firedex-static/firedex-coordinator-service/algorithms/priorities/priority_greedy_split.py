
class PriorityGreedySplit:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, experiment_configuration, network_flows):
        priorities = range(1, 1 + firedex_configuration["priorities"])

        network_flows = sorted(
                               network_flows,
                               key = lambda subscriber_network_flow: subscriber_network_flow["network_flow"]["utility_function"],
                               reverse = True
                              )

        grouped_network_flows = self.__even_group_split(network_flows, priorities.__len__())

        new_network_flows = []

        for priority, network_flows in zip(priorities, grouped_network_flows):
            for network_flow in network_flows:
                network_flow["priority"] = priority
                new_network_flows.append(network_flow)

        return new_network_flows

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


class PriorityGreedySplit:

    def __init__(self):
        pass

    def apply(self, firedex_configuration, network_flows):
        priorities = range( 1, 1 + firedex_configuration.priorities() )

        network_flows.sort(
            key = lambda x: x.adjusted_utility_function(),
            reverse = True
        )

        grouped_network_flows = self.__even_group_split(
            network_flows = network_flows,
            groups = priorities.__len__()
        )

        for priority, network_flows in zip(priorities, grouped_network_flows):
            for network_flow in network_flows:
                network_flow.set_priority(priority = priority)

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

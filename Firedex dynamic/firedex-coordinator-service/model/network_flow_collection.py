
class NetworkFlowCollection:

    def __init__(self):
        self.__network_flows = []

    def network_flows(self):
        return self.__network_flows

    def network_flows_by_subscriber(self, subscriber):
        network_flows_by_subscriber = []

        for network_flow in self.network_flows():
            if network_flow.subscriber() == subscriber:
                network_flows_by_subscriber.append(network_flow)

        return network_flows_by_subscriber

    def network_flows_by_not_subscriber(self, subscriber):
        network_flows_by_not_subscriber = []

        for network_flow in self.network_flows():
            if network_flow.subscriber() != subscriber:
                network_flows_by_not_subscriber.append(network_flow)

        return network_flows_by_not_subscriber

    def subscriptions(self):
        subscriptions = []

        for network_flow in self.network_flows():
            for subscription in network_flow.subscriptions():
                subscriptions.append(subscription)

        return subscriptions

    def subscriptions_by_subscriber(self, subscriber):
        subscriptions_by_subscriber = []

        for network_flow in self.network_flows_by_subscriber(subscriber = subscriber):
            for subscription in network_flow.subscriptions():
                subscriptions_by_subscriber.append(subscription)

        return subscriptions_by_subscriber

    def subscriptions_by_not_subscriber(self, subscriber):
        subscriptions_by_not_subscriber = []

        for network_flow in self.network_flows_by_not_subscriber(subscriber = subscriber):
            for subscription in network_flow.subscriptions():
                subscriptions_by_not_subscriber.append(subscription)

        return subscriptions_by_not_subscriber

    def add_network_flows(self, network_flows):
        for network_flow in network_flows:
            self.network_flows().append(network_flow)

    def remove_network_flows(self, network_flows):
        for network_flow in network_flows:
            self.network_flows().remove(network_flow)

    def replace_network_flows(self, old_network_flows, new_network_flows):
        self.remove_network_flows(old_network_flows)
        self.add_network_flows(new_network_flows)

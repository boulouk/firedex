
import random

class NetworkFlowRandom:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, experiment_configuration):
        network_flows = range(10001, 10001 + firedex_configuration["network_flows"])

        result = []

        experiment_subscribers = experiment_configuration["subscribers"]
        for experiment_subscriber in experiment_subscribers:
            subscriber = experiment_subscriber["subscriber"]

            identifier = subscriber["identifier"]
            host = subscriber["host"]

            for port in network_flows:
                subscriber_network_flow = {
                    "identifier": identifier,
                    "network_flow": {
                        "host": host,
                        "port": port,
                        "utility_function": 0
                    },
                    "subscriptions": []
                }
                result.append(subscriber_network_flow)

        for experiment_subscriber in experiment_subscribers:
            subscriber = experiment_subscriber["subscriber"]

            identifier = subscriber["identifier"]
            host = subscriber["host"]

            subscriber_network_flows = self.__subscriber_network_flows(result, identifier)

            experiment_subscriptions = subscriber["subscriptions"]
            for experiment_subscription in experiment_subscriptions:
                topic = experiment_subscription["topic"]
                utility_function = experiment_subscription["utilityFunction"]
                port = random.sample(network_flows, 1)[0]

                subscriber_network_flow = self.__subscriber_network_flow(subscriber_network_flows, host, port)

                network_flow = subscriber_network_flow["network_flow"]
                subscriptions = subscriber_network_flow["subscriptions"]

                network_flow["utility_function"] = network_flow["utility_function"] + utility_function
                subscriptions.append({
                    "topic": topic,
                    "utility_function": utility_function
                })

        result = self.__remove_empty_network_flows(result)

        return result

    def __subscriber_network_flows(self, result, identifier):
        subscriber_network_flows = []

        for subscriber_network_flow in result:
            subscriber_identifer = subscriber_network_flow["identifier"]
            if subscriber_identifer == identifier:
                subscriber_network_flows.append(subscriber_network_flow)

        return subscriber_network_flows

    def __subscriber_network_flow(self, subscriber_network_flows, host, port):
        for subscriber_network_flow in subscriber_network_flows:
            subscriber_host = subscriber_network_flow["network_flow"]["host"]
            subscriber_port = subscriber_network_flow["network_flow"]["port"]
            if subscriber_host == host and subscriber_port == port:
                return subscriber_network_flow

        return None

    def __remove_empty_network_flows(self, result):
        new_result = []
        for subscriber_network_flow in result:
            subscriptions = subscriber_network_flow["subscriptions"]
            if subscriptions:
                new_result.append(subscriber_network_flow)
        return new_result

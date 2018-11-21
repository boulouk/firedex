
import json
import requests

from flask import Flask, request, jsonify

from algorithms.network_flows.network_flow_random import NetworkFlowRandom
from algorithms.network_flows.network_flow_greedy_split import NetworkFlowGreedySplit
from algorithms.priorities.priority_random import PriorityRandom
from algorithms.priorities.priority_greedy_split import PriorityGreedySplit
from algorithms.priorities.priority_greedy_split_local import PriorityGreedySplitLocal
from algorithms.drop_rates.drop_rate_flat import DropRateFlat
from algorithms.drop_rates.drop_rate_linear import DropRateLinear
from algorithms.drop_rates.drop_rate_exponential import DropRateExponential


application = Flask("firedex-middleware")

class Configuration:

    def __init__(self):
        self.network_configuration = None
        self.topology_configuration = None
        self.firedex_configuration = None
        self.experiment_configuration = None

        self.network_flows = None

configuration = Configuration()


@application.route("/api/firedex/push-network-configuration/", methods = ["POST"])
def push_network_configuration():
    json_request = request.json

    network_configuration = json.loads(json_request)
    configuration.network_configuration = network_configuration

    return jsonify( {"result": "successful"} )

@application.route("/api/firedex/push-topology-configuration/", methods = ["POST"])
def push_topology_configuration():
    json_request = request.json

    topology_configuration = json.loads(json_request)
    configuration.topology_configuration = topology_configuration

    return jsonify( {"result": "successful"} )

@application.route("/api/firedex/push-firedex-configuration/", methods = ["POST"])
def push_firedex_configuration():
    json_request = request.json

    firedex_configuration = json.loads(json_request)
    configuration.firedex_configuration = firedex_configuration

    return jsonify( {"result": "successful"} )

@application.route("/api/firedex/push-experiment-configuration/", methods = ["POST"])
def push_experiment_configuration():
    json_request = request.json

    experiment_configuration = json.loads(json_request)
    configuration.experiment_configuration = experiment_configuration

    return jsonify( {"result": "successful"} )

def __network_flow_algorithm():
    algorithm_name = configuration.firedex_configuration["network_flow_algorithm"]
    if algorithm_name == "random":
        return NetworkFlowRandom()
    if algorithm_name == "greedy_split":
        return NetworkFlowGreedySplit()

    return None

def __priority_algorithm():
    algorithm_name = configuration.firedex_configuration["priority_algorithm"]
    if algorithm_name == "random":
        return PriorityRandom()
    if algorithm_name == "greedy_split":
        return PriorityGreedySplit()
    if algorithm_name == "greedy_split_local":
        return PriorityGreedySplitLocal()

    return None

def __drop_rate_algorithm():
    algorithm_name = configuration.firedex_configuration["drop_rate_algorithm"]
    if algorithm_name == "flat":
        return DropRateFlat()
    if algorithm_name == "linear":
        return DropRateLinear()
    if algorithm_name == "exponential":
        return DropRateExponential()

    return None

@application.route("/api/firedex/apply-experiment-configuration/", methods = ["POST"])
def apply_experiment_configuration():
    network_flow_algorithm = __network_flow_algorithm()
    priority_algorithm = __priority_algorithm()
    drop_rate_algorithm = __drop_rate_algorithm()

    __network_flows = network_flow_algorithm.apply(
                                                 configuration.network_configuration,
                                                 configuration.firedex_configuration,
                                                 configuration.experiment_configuration
                                                )

    __network_flows = priority_algorithm.apply(
                                             configuration.network_configuration,
                                             configuration.firedex_configuration,
                                             configuration.experiment_configuration,
                                             __network_flows
                                            )

    __network_flows = drop_rate_algorithm.apply(
                                              configuration.network_configuration,
                                              configuration.firedex_configuration,
                                              configuration.experiment_configuration,
                                              __network_flows
                                             )

    configuration.network_flows = __network_flows

    # Push system configuration to the SDN controller.
    url = "http://127.0.0.1:8080/api/flow/push-configuration/"
    data = json.dumps(__network_flows)
    requests.post(url, data = data)
    # ---

    return jsonify(__network_flows)

def __network_flows_by_identifier(identifier):
    network_flows_by_identifier = []

    for network_flow in configuration.network_flows:
        subscriber_identifier = network_flow["identifier"]
        if subscriber_identifier == identifier:
            network_flows_by_identifier.append(network_flow)

    return network_flows_by_identifier

def __network_flow_by_topic(network_flows, topic):
    for network_flow in network_flows:
        subscriptions = network_flow["subscriptions"]
        for subscription in subscriptions:
            subscription_topic = subscription["topic"]
            if subscription_topic == topic:
                return network_flow

    return None

@application.route("/api/firedex/subscriber-network-flows/", methods = ["POST"])
def subscriber_network_flows():
    json_request = request.json

    identifier = json_request["identifier"]
    subscriptions = json_request["subscriptions"]

    result = {
        "identifier": identifier,
        "firedexSubscriptions": []
    }

    network_flows_by_identifier = __network_flows_by_identifier(identifier)
    firedex_subscriptions = []

    for subscription in subscriptions:
        topic = subscription["topic"]
        network_flow_by_topic = __network_flow_by_topic(network_flows_by_identifier, topic)
        firedex_subscriptions.append({
            "topic": topic,
            "port": network_flow_by_topic["network_flow"]["port"]
        })

    result["firedexSubscriptions"] = firedex_subscriptions
    print(firedex_subscriptions)

    return jsonify(result)

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 8888, debug = True)

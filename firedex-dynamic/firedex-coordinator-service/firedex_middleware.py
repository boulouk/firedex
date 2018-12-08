
import json
import threading

from flask import Flask, request, jsonify

from algorithms.network_flows.network_flow_random import NetworkFlowRandom
from algorithms.network_flows.network_flow_greedy_split import NetworkFlowGreedySplit
from algorithms.priorities.priority_random import PriorityRandom
from algorithms.priorities.priority_greedy_split import PriorityGreedySplit
from algorithms.priorities.priority_cluster_split import PriorityClusterSplit
from algorithms.drop_rates.drop_rate_flat import DropRateFlat
from algorithms.drop_rates.drop_rate_linear import DropRateLinear
from algorithms.drop_rates.drop_rate_exponential import DropRateExponential
from algorithms.drop_rates.drop_rate_optimized import DropRateOptimized

from configuration.controller_configuration import ControllerConfiguration
from configuration.firedex_configuration import FiredexConfiguration
from configuration.network_configuration import NetworkConfiguration
from configuration.publishers_configuration import PublishersConfiguration
from configuration.subscribers_configuration import SubscribersConfiguration

from model.subscription import Subscription

from sdn.controller_interface import ControllerInterface

application = Flask("firedex-coordinator-service")

class Configuration:

    def __init__(self):
        self.network_configuration = None
        self.controller_configuration = None
        self.firedex_configuration = None

        self.publishers_configuration = None
        self.subscribers_configuration = None

configuration = Configuration()

class Transaction:

    def __init__(self):
        self.lock = threading.Lock()
        self.old_network_flows = None
        self.new_network_flows = None

transaction = Transaction()

def __network_flow_algorithm(network_flow_algorithm):
    if network_flow_algorithm == "random":
        return NetworkFlowRandom()
    elif network_flow_algorithm == "greedy_split":
        return NetworkFlowGreedySplit()

    # should not reach this line

def __priority_algorithm(priority_algorithm):
    if priority_algorithm == "random":
        return PriorityRandom()
    elif priority_algorithm == "greedy_split":
        return PriorityGreedySplit()
    elif priority_algorithm == "cluster_split":
        return PriorityClusterSplit()

    # should not reach this line

def __drop_rate_algorithm(drop_rate_algorithm):
    if drop_rate_algorithm == "flat":
        return DropRateFlat()
    elif drop_rate_algorithm == "linear":
        return DropRateLinear()
    elif drop_rate_algorithm == "exponential":
        return DropRateExponential()
    elif drop_rate_algorithm == "optimized":
        return DropRateOptimized()

    # should not reach this line

@application.route("/api/firedex/push-experiment-configuration/", methods = ["POST"])
def push_experiment_configuration():
    json_request = request.json

    experiment_configuration = json.loads(json_request)
    network_configuration = experiment_configuration["network_configuration"]
    controller_configuration = experiment_configuration["controller_configuration"]
    firedex_configuration = experiment_configuration["firedex_configuration"]

    bandwidth = network_configuration["bandwidth"]
    delay = network_configuration["delay"]
    error_rate = network_configuration["error_rate"]

    configuration.network_configuration = NetworkConfiguration(
        bandwidth = bandwidth,
        delay = delay,
        error_rate = error_rate
    )

    host = controller_configuration["host"]
    port = controller_configuration["port"]
    switch_identifier = controller_configuration["switch_identifier"]

    configuration.controller_configuration = ControllerConfiguration(
        host = host,
        port = port,
        switch_identifier = switch_identifier
    )

    network_flows = firedex_configuration["network_flows"]
    priorities = firedex_configuration["priorities"]
    network_flow_algorithm = firedex_configuration["network_flow_algorithm"]
    priority_algorithm = firedex_configuration["priority_algorithm"]
    drop_rate_algorithm = firedex_configuration["drop_rate_algorithm"]
    rho_tolerance = firedex_configuration["rho_tolerance"]

    configuration.firedex_configuration = FiredexConfiguration(
        network_flows = network_flows,
        priorities = priorities,
        network_flow_algorithm = __network_flow_algorithm(network_flow_algorithm = network_flow_algorithm),
        priority_algorithm = __priority_algorithm(priority_algorithm = priority_algorithm),
        drop_rate_algorithm = __drop_rate_algorithm(drop_rate_algorithm = drop_rate_algorithm),
        rho_tolerance = rho_tolerance
    )

    configuration.publishers_configuration = PublishersConfiguration()
    configuration.subscribers_configuration = SubscribersConfiguration()

    return jsonify( {"result": "successful"} )

# PUBLISHER API

@application.route("/api/firedex/publication-intention/", methods = ["POST"])
def publication_intention():
    transaction.lock.acquire()

    json_request = request.json
    publication_intention = json_request

    publication_collection = configuration.publishers_configuration.publication_collection()

    publisher = publication_intention["identifier"]
    publications = publication_intention["publications"]
    for publication in publications:
        topic = publication["topic"]
        rate = publication["rate"]
        message_size = publication["messageSize"]

        publication_collection.add_publication(
            publisher = publisher,
            topic = topic,
            rate = rate,
            message_size = message_size
        )

    transaction.lock.release()

    return jsonify( {"result": "successful"} )

@application.route("/api/firedex/publication-completion/", methods = ["POST"])
def publication_completion():
    transaction.lock.acquire()

    json_request = request.json
    publication_completed = json_request

    publication_collection = configuration.publishers_configuration.publication_collection()

    publisher = publication_completed["identifier"]
    publications = publication_completed["publications"]
    for publication in publications:
        topic = publication["topic"]

        publication_collection.remove_publication(
            publisher = publisher,
            topic = topic
        )

    transaction.lock.release()

    return jsonify( {"result": "successful"} )

# ---

# SUBSCRIBER API

@application.route("/api/firedex/subscription-intention/insert/", methods = ["POST"])
def subscription_intention_insert():
    transaction.lock.acquire()

    json_request = request.json
    subscription_intention = json_request

    publishers_configuration = configuration.publishers_configuration
    publication_collection = publishers_configuration.publication_collection()
    subscribers_configuration = configuration.subscribers_configuration

    subscriptions_to_insert = []

    subscriber = subscription_intention["identifier"]
    host = subscription_intention["host"]
    subscriptions = subscription_intention["subscriptions"]
    for subscription in subscriptions:
        topic = subscription["topic"]
        utility_function = subscription["utilityFunction"]

        publications_load_by_topic = publication_collection.publications_load_by_topic(topic = topic)
        if publications_load_by_topic == 0:
            adjusted_utility_function = 0
        else:
            adjusted_utility_function = float(utility_function) / float(publications_load_by_topic)

        subscription_to_insert = Subscription(
            subscriber = subscriber,
            topic = topic,
            utility_function = utility_function,
            adjusted_utility_function = adjusted_utility_function
        )

        subscriptions_to_insert.append(subscription_to_insert)

    network_flow_collection = subscribers_configuration.network_flow_collection()

    old_network_flows = network_flow_collection.network_flows_by_subscriber(subscriber = subscriber)
    old_subscriptions = network_flow_collection.subscriptions_by_subscriber(subscriber = subscriber)

    subscriptions = old_subscriptions + subscriptions_to_insert

    network_flow_algorithm = configuration.firedex_configuration.network_flow_algorithm()
    network_flows = network_flow_algorithm.apply(
        firedex_configuration = configuration.firedex_configuration,
        subscriber = subscriber,
        host = host,
        subscriber_subscriptions = subscriptions
    )

    response = {
        "identifier": subscriber,
        "host": host,
        "modifiedSubscriptions": [],
        "insertedSubscriptions": []
    }

    for old_subscription in old_subscriptions:
        topic = old_subscription.topic()
        old_port = __network_flow_port_by_subscription(
            network_flows = old_network_flows,
            subscription = old_subscription
        )

        new_port = __network_flow_port_by_subscription(
            network_flows = network_flows,
            subscription = old_subscription
        )

        if old_port != new_port:
            modified_subscription = {
                "topic": topic,
                "oldPort": old_port,
                "newPort": new_port
            }

            response["modifiedSubscriptions"].append(modified_subscription)

    for subscription_to_insert in subscriptions_to_insert:
        topic = subscription_to_insert.topic()
        port = __network_flow_port_by_subscription(
            network_flows = network_flows,
            subscription = subscription_to_insert
        )

        inserted_subscription = {
            "topic": topic,
            "port": port
        }

        response["insertedSubscriptions"].append(inserted_subscription)

    controller_interface = ControllerInterface(
        host = configuration.controller_configuration.host(),
        port = configuration.controller_configuration.port(),
        switch_identifier = configuration.controller_configuration.switch_identifier()
    )
    controller_interface.remove_firedex_policies(network_flows = old_network_flows)

    transaction.old_network_flows = old_network_flows
    transaction.new_network_flows = network_flows

    return jsonify(response)

@application.route("/api/firedex/subscription-intention/modify/", methods = ["POST"])
def subscription_intention_modify():
    transaction.lock.acquire()

    json_request = request.json
    subscription_intention = json_request

    publishers_configuration = configuration.publishers_configuration
    publication_collection = publishers_configuration.publication_collection()
    subscribers_configuration = configuration.subscribers_configuration

    subscriptions_to_modify = []

    subscriber = subscription_intention["identifier"]
    host = subscription_intention["host"]
    subscriptions = subscription_intention["subscriptions"]
    for subscription in subscriptions:
        topic = subscription["topic"]
        utility_function = subscription["utilityFunction"]

        publications_load_by_topic = publication_collection.publications_load_by_topic(topic = topic)
        if publications_load_by_topic == 0:
            adjusted_utility_function = 0
        else:
            adjusted_utility_function = float(utility_function) / float(publications_load_by_topic)

        subscription_to_modify = Subscription(
            subscriber = subscriber,
            topic = topic,
            utility_function = utility_function,
            adjusted_utility_function = adjusted_utility_function
        )

        subscriptions_to_modify.append(subscription_to_modify)

    network_flow_collection = subscribers_configuration.network_flow_collection()

    old_network_flows = network_flow_collection.network_flows_by_subscriber(subscriber = subscriber)
    old_subscriptions = network_flow_collection.subscriptions_by_subscriber(subscriber = subscriber)

    subscriptions = [subscription for subscription in old_subscriptions if subscription not in subscriptions_to_modify]
    subscriptions = subscriptions + subscriptions_to_modify

    network_flow_algorithm = configuration.firedex_configuration.network_flow_algorithm()
    network_flows = network_flow_algorithm.apply(
        firedex_configuration = configuration.firedex_configuration,
        subscriber = subscriber,
        host = host,
        subscriber_subscriptions = subscriptions
    )

    response = {
        "identifier": subscriber,
        "host": host,
        "modifiedSubscriptions": []
    }

    for old_subscription in old_subscriptions:
        topic = old_subscription.topic()
        old_port = __network_flow_port_by_subscription(
            network_flows = old_network_flows,
            subscription = old_subscription
        )

        new_port = __network_flow_port_by_subscription(
            network_flows = network_flows,
            subscription = old_subscription
        )

        if old_port != new_port:
            modified_subscription = {
                "topic": topic,
                "oldPort": old_port,
                "newPort": new_port
            }

            response["modifiedSubscriptions"].append(modified_subscription)

    controller_interface = ControllerInterface(
        host = configuration.controller_configuration.host(),
        port = configuration.controller_configuration.port(),
        switch_identifier = configuration.controller_configuration.switch_identifier()
    )
    controller_interface.remove_firedex_policies(network_flows = old_network_flows)

    transaction.old_network_flows = old_network_flows
    transaction.new_network_flows = network_flows

    return jsonify(response)

@application.route("/api/firedex/subscription-intention/remove/", methods = ["POST"])
def subscription_intention_remove():
    transaction.lock.acquire()

    json_request = request.json
    subscription_intention = json_request

    publishers_configuration = configuration.publishers_configuration
    publication_collection = publishers_configuration.publication_collection()
    subscribers_configuration = configuration.subscribers_configuration

    subscriptions_to_remove = []

    subscriber = subscription_intention["identifier"]
    host = subscription_intention["host"]
    subscriptions = subscription_intention["subscriptions"]
    for subscription in subscriptions:
        topic = subscription["topic"]
        subscriptions_to_remove.append(topic)

    network_flow_collection = subscribers_configuration.network_flow_collection()

    old_network_flows = network_flow_collection.network_flows_by_subscriber(subscriber = subscriber)
    old_subscriptions = network_flow_collection.subscriptions_by_subscriber(subscriber = subscriber)

    subscriptions = [subscription for subscription in old_subscriptions if subscription.topic() not in subscriptions_to_remove]

    network_flow_algorithm = configuration.firedex_configuration.network_flow_algorithm()
    network_flows = network_flow_algorithm.apply(
        firedex_configuration = configuration.firedex_configuration,
        subscriber = subscriber,
        host = host,
        subscriber_subscriptions = subscriptions
    )

    response = {
        "identifier": subscriber,
        "host": host,
        "modifiedSubscriptions": [],
        "removedSubscriptions": []
    }

    for subscription in subscriptions:
        topic = subscription.topic()
        old_port = __network_flow_port_by_subscription(
            network_flows = old_network_flows,
            subscription = subscription
        )

        new_port = __network_flow_port_by_subscription(
            network_flows = network_flows,
            subscription = subscription
        )

        if old_port != new_port:
            modified_subscription = {
                "topic": topic,
                "oldPort": old_port,
                "newPort": new_port
            }

            response["modifiedSubscriptions"].append(modified_subscription)

    for subscription_to_remove in subscriptions_to_remove:
        topic = subscription_to_remove

        port = __network_flow_port_by_topic(
            network_flows = old_network_flows,
            topic = topic
        )

        removed_subscription = {
            "topic": topic,
            "port": port
        }

        response["removedSubscriptions"].append(removed_subscription)

    controller_interface = ControllerInterface(
        host = configuration.controller_configuration.host(),
        port = configuration.controller_configuration.port(),
        switch_identifier = configuration.controller_configuration.switch_identifier()
    )
    controller_interface.remove_firedex_policies(network_flows = old_network_flows)

    transaction.old_network_flows = old_network_flows
    transaction.new_network_flows = network_flows

    return jsonify(response)

def __network_flow_port_by_subscription(network_flows, subscription):
    for network_flow in network_flows:
        subscriptions = network_flow.subscriptions()
        if subscription in subscriptions:
            return network_flow.port()

    # should not reach this line

def __network_flow_port_by_topic(network_flows, topic):
    for network_flow in network_flows:
        subscriptions = network_flow.subscriptions()
        for subscription in subscriptions:
            if subscription.topic() == topic:
                return network_flow.port()

    # should not reach this line

@application.route("/api/firedex/subscription-completion/", methods = ["POST"])
def subscription_completion():
    json_request = request.json
    subscription_completed = json_request

    subscriber = subscription_completed["identifier"]
    host = subscription_completed["host"]

    subscribers_configuration = configuration.subscribers_configuration
    network_flow_collection = subscribers_configuration.network_flow_collection()
    network_flow_collection.replace_network_flows(
        old_network_flows = transaction.old_network_flows,
        new_network_flows = transaction.new_network_flows
    )

    network_flows = network_flow_collection.network_flows()

    priority_algorithm = configuration.firedex_configuration.priority_algorithm()
    priority_algorithm.apply(
        firedex_configuration = configuration.firedex_configuration,
        network_flows = network_flows
    )

    drop_rate_algorithm = configuration.firedex_configuration.drop_rate_algorithm()
    drop_rate_algorithm.apply(
        network_configuration = configuration.network_configuration,
        firedex_configuration = configuration.firedex_configuration,
        publishers_configuration = configuration.publishers_configuration,
        network_flows = network_flows
    )

    drop_rate_algorithm = DropRateExponential()
    drop_rate_algorithm.apply(
        network_configuration = configuration.network_configuration,
        firedex_configuration = configuration.firedex_configuration,
        publishers_configuration = configuration.publishers_configuration,
        network_flows = network_flows
    )

    controller_interface = ControllerInterface(
        host = configuration.controller_configuration.host(),
        port = configuration.controller_configuration.port(),
        switch_identifier = configuration.controller_configuration.switch_identifier()
    )
    network_flows_by_subscriber = network_flow_collection.network_flows_by_subscriber(subscriber = subscriber)
    network_flows_by_not_subscriber = network_flow_collection.network_flows_by_not_subscriber(subscriber = subscriber)
    controller_interface.add_firedex_policies(network_flows = network_flows_by_subscriber)
    controller_interface.modify_firedex_policies(network_flows = network_flows_by_not_subscriber)

    for network_flow in network_flows:
        print( network_flow.host(), network_flow.port(), network_flow.get_priority(), network_flow.get_drop_rate() )

    transaction.lock.release()

    return jsonify( {"result": "successful"} )

# ---

if __name__ == "__main__":
    application.run( host = "0.0.0.0", port = 8888, debug = True )

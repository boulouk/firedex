
import numpy as numpy
import cvxpy as cvxpy
import time

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

from model.network_flow import NetworkFlow
from model.network_flow_collection import NetworkFlowCollection
from model.publication import Publication
from model.publication_collection import PublicationCollection
from model.subscription import Subscription

NETWORK_FLOW_ALGORITHM = "greedy_split"
NETWORK_FLOWS = 7
PRIORITY_ALGORITHM = "greedy_split"
PRIORITIES = 7

SUBSCRIBERS = 10

# DROP_RATE_ALGORITHMS = ["flat", "linear", "exponential", "optimized"]
DROP_RATE_ALGORITHMS = ["linear", "exponential", "optimized"]
BANDWIDTH = 1000 * 120 # rho = 1.7
RHO_TOLERANCE = 0.1

EXPERIMENTS = 100000
COUNT = 3

CURRENT_DROP_RATE_ALGORITHM = ""

ACHIEVED_UTILITIES = []
MAX_ACHIEVED_UTILITIES = []

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

def run_experiment():
    network_flow_algorithm = __network_flow_algorithm(network_flow_algorithm = NETWORK_FLOW_ALGORITHM)
    priority_algorithm = __priority_algorithm(priority_algorithm = PRIORITY_ALGORITHM)
    drop_rate_algorithm = __drop_rate_algorithm(drop_rate_algorithm = CURRENT_DROP_RATE_ALGORITHM)

    network_configuration = NetworkConfiguration(
        bandwidth = BANDWIDTH,
        delay = 0,
        error_rate = 0
    )

    firedex_configuration = FiredexConfiguration(
        network_flows = NETWORK_FLOWS,
        priorities = PRIORITIES,
        network_flow_algorithm = NETWORK_FLOW_ALGORITHM,
        priority_algorithm = PRIORITY_ALGORITHM,
        drop_rate_algorithm = CURRENT_DROP_RATE_ALGORITHM,
        rho_tolerance = RHO_TOLERANCE
    )

    TOPIC = []
    for topic_index in range(1, 21 + 1):
        TOPIC.append( "topic%d" % topic_index )

    publishers_configuration = PublishersConfiguration()
    for topic in TOPIC:
        publishers_configuration.publication_collection().add_publication(
            publisher = "publisher",
            topic = topic,
            rate = 10,
            message_size = 51
        )

    subscriptions = []

    for subscriber_index in range(SUBSCRIBERS):
        subscriber = "subscriber%d" % subscriber_index
        host = "10.0.0.%d" % subscriber_index

        for topic_index in range(1, 21 + 1):
            topic = "topic%d" % topic_index
            utility_function = __random_utility_function(0.01, 100)

            publication_collection = publishers_configuration.publication_collection()
            publications_load_by_topic = publication_collection.publications_load_by_topic(topic = topic)
            adjusted_utility_function = float(utility_function) / float(publications_load_by_topic)

            random_subscription = Subscription(
                subscriber = subscriber,
                topic = topic,
                utility_function = utility_function,
                adjusted_utility_function = adjusted_utility_function
            )

            subscriptions.append(random_subscription)

    network_flows = []

    for subscriber_index in range(SUBSCRIBERS):
        subscriber = "subscriber%d" % subscriber_index
        host = "10.0.0.%d" % subscriber_index

        subscriber_subscriptions = __subscriber_subscriptions(subscriber, subscriptions)

        subscriber_network_flows = network_flow_algorithm.apply(
            firedex_configuration = firedex_configuration,
            subscriber = subscriber,
            host = host,
            subscriber_subscriptions = subscriber_subscriptions
        )

        network_flows.extend(subscriber_network_flows)

    priority_algorithm.apply(
        firedex_configuration = firedex_configuration,
        network_flows = network_flows
    )

    drop_rate_algorithm.apply(
        network_configuration = network_configuration,
        firedex_configuration = firedex_configuration,
        publishers_configuration = publishers_configuration,
        network_flows = network_flows
    )

    sum_achieved_utility = 0
    max_achieved_utility = 0
    for network_flow in network_flows:
        sum_achieved_utility += __achieved_utility(network_flow)
        network_flow.set_drop_rate(0)
        max_achieved_utility += __achieved_utility(network_flow)

    ACHIEVED_UTILITIES.append(sum_achieved_utility)
    MAX_ACHIEVED_UTILITIES.append(max_achieved_utility)

def __random_utility_function(lower_bound, upper_bound):
    value = numpy.random.uniform(lower_bound, upper_bound)
    return value

def __subscriber_subscriptions(subscriber, subscriptions):
    subscriber_subscriptions = []

    for subscription in subscriptions:
        if subscription.subscriber() == subscriber:
            subscriber_subscriptions.append(subscription)

    return subscriber_subscriptions

def __network_flows_by_priority(network_flows):
    network_flows_by_priority = {}

    for priority in range(1, PRIORITIES + 1):
        network_flows_by_priority[priority] = []

    for network_flow in network_flows:
        priority = network_flow.get_priority()
        network_flows_by_priority[priority].append(network_flow)

    return network_flows_by_priority

def __achieved_utility(network_flow):
    success_rate = 1 - network_flow.get_drop_rate()
    achieved_utility = float( network_flow.adjusted_utility_function() ) * float( cvxpy.log1p(success_rate).value )
    return achieved_utility


if __name__ == "__main__":
    for drop_rate_algorithm in DROP_RATE_ALGORITHMS:
        print("algorithm: %s" % drop_rate_algorithm)

        CURRENT_DROP_RATE_ALGORITHM = drop_rate_algorithm

        for t in range(COUNT):
            print("Experiment: %d" % t)

            start = int( round( time.time() * 1000 ) )

            for i in range(EXPERIMENTS):
                run_experiment()

            end = int( round( time.time() * 1000 ) )

            execution_time = (end - start)

            average_achieved_utility = numpy.mean( [ achieved_utility for achieved_utility in ACHIEVED_UTILITIES ] )
            average_max_achieved_utility = numpy.mean([max_achieved_utility for max_achieved_utility in MAX_ACHIEVED_UTILITIES])

            print("---")
            print("achieved-utility: ", average_achieved_utility)
            print("max-achieved-utility: ", average_max_achieved_utility)
            print("execution-time: ", execution_time)
            print("---")

            ACHIEVED_UTILITIES = []
            MAX_ACHIEVED_UTILITIES = []

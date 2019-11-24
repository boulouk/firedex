
import numpy as numpy
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

SUBSCRIBERS = 10

PRIORITY_ALGORITHMS = ["random", "greedy_split", "cluster_split"]
PRIORITIES = [1, 2, 3, 4, 5, 6, 7]

EXPERIMENTS = 100000
COUNT = 3

CURRENT_PRIORITY_ALGORITHM = ""
CURRENT_PRIORITIES = 0

INTRA_VARIANCES = []
INTER_VARIANCES = []
VARIANCES = []

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

def run_experiment():
    network_flow_algorithm = __network_flow_algorithm(network_flow_algorithm = NETWORK_FLOW_ALGORITHM)
    priority_algorithm = __priority_algorithm(priority_algorithm = CURRENT_PRIORITY_ALGORITHM)

    firedex_configuration = FiredexConfiguration(
        network_flows = NETWORK_FLOWS,
        priorities = CURRENT_PRIORITIES,
        network_flow_algorithm = NETWORK_FLOW_ALGORITHM,
        priority_algorithm = CURRENT_PRIORITY_ALGORITHM,
        drop_rate_algorithm = "",
        rho_tolerance = 0
    )

    subscriptions = []

    for subscriber_index in range(SUBSCRIBERS):
        subscriber = "subscriber%d" % subscriber_index
        host = "10.0.0.%d" % subscriber_index

        for i in range(21):
            random_subscription = __random_subscription(subscriber, "topic")
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

    mean = numpy.mean( [ network_flow.utility_function() for network_flow in network_flows ] )
    variance = numpy.var( [ network_flow.utility_function() for network_flow in network_flows ] )

    network_flows_by_priority = __network_flows_by_priority(network_flows)

    intra_variance = 0
    for priority in network_flows_by_priority.keys():
        weight = float( network_flows_by_priority[priority].__len__() ) / float( network_flows.__len__() )
        current_variance = numpy.var( [ network_flow.utility_function() for network_flow in network_flows_by_priority[priority] ] )
        intra_variance += weight * current_variance

    inter_variance = 0
    for priority in network_flows_by_priority.keys():
        weight = float( network_flows_by_priority[priority].__len__() ) / float( network_flows.__len__() )
        current_mean = numpy.mean( [ network_flow.utility_function() for network_flow in network_flows_by_priority[priority] ] )
        inter_variance += weight * ( (current_mean - mean) ** 2 )

    # print("intra-variance: ", intra_variance)
    # print("inter-variance: ", inter_variance)
    # print( intra_variance + inter_variance, variance )

    INTRA_VARIANCES.append(intra_variance)
    INTER_VARIANCES.append(inter_variance)
    VARIANCES.append(variance)

def __random_subscription(subscriber, topic):
    utility_function = __uniform(0.01, 100)
    adjusted_utility_function = utility_function

    subscription = Subscription(
        subscriber = subscriber,
        topic = topic,
        utility_function = utility_function,
        adjusted_utility_function = adjusted_utility_function
    )

    return subscription

def __uniform(lower_bound, upper_bound):
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

    for priority in range(1, CURRENT_PRIORITIES + 1):
        network_flows_by_priority[priority] = []

    for network_flow in network_flows:
        priority = network_flow.get_priority()
        network_flows_by_priority[priority].append(network_flow)

    return network_flows_by_priority

if __name__ == "__main__":
    for priority_algorithm in PRIORITY_ALGORITHMS:
        print("algorithm: %s" % priority_algorithm)

        CURRENT_PRIORITY_ALGORITHM = priority_algorithm

        for current_priority in PRIORITIES:
            print("priorities: %d" % current_priority)

            CURRENT_PRIORITIES = current_priority

            for t in range(COUNT):
                print("Experiment: %d" % t)

                start = int( round( time.time() * 1000 ) )

                for i in range(EXPERIMENTS):
                    run_experiment()

                end = int( round( time.time() * 1000 ) )

                execution_time = (end - start)

                mean_intra_variance = numpy.mean([intra_variance for intra_variance in INTRA_VARIANCES])
                mean_inter_variance = numpy.mean([inter_variance for inter_variance in INTER_VARIANCES])
                mean_variance = numpy.mean([variance for variance in VARIANCES])

                print("---")
                print("intra-variance: ", mean_intra_variance)
                print("inter-variance: ", mean_inter_variance)
                print(mean_intra_variance + mean_inter_variance, mean_variance)
                print("execution-time: ", execution_time)
                print("---")

                INTRA_VARIANCES = []
                INTER_VARIANCES = []
                VARIANCES = []

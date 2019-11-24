
import numpy as numpy
import time

from algorithms.network_flows.network_flow_random import NetworkFlowRandom
from algorithms.network_flows.network_flow_greedy_split import NetworkFlowGreedySplit
from configuration.firedex_configuration import FiredexConfiguration

from model.subscription import Subscription

NETWORK_FLOW_ALGORITHMS = ["random", "greedy_split"]
NETWORK_FLOWS = [1, 2, 3, 4, 5, 6, 7]

EXPERIMENTS = 100000
COUNT = 3

CURRENT_NETWORK_FLOW_ALGORITHM = ""
CURRENT_NETWORK_FLOWS = 0

INTRA_VARIANCES = []
INTER_VARIANCES = []
VARIANCES = []

def __network_flow_algorithm(network_flow_algorithm):
    if network_flow_algorithm == "random":
        return NetworkFlowRandom()
    elif network_flow_algorithm == "greedy_split":
        return NetworkFlowGreedySplit()

    # should not reach this line

def run_experiment():
    network_flow_algorithm = __network_flow_algorithm(network_flow_algorithm = CURRENT_NETWORK_FLOW_ALGORITHM)

    firedex_configuration = FiredexConfiguration(
        network_flows = CURRENT_NETWORK_FLOWS,
        priorities = 0,
        network_flow_algorithm = CURRENT_NETWORK_FLOW_ALGORITHM,
        priority_algorithm = "",
        drop_rate_algorithm = "",
        rho_tolerance = 0
    )

    SUBSCRIBER = "subscriber1"
    HOST = "10.0.0.1"
    subscriptions = []

    for i in range(21):
        random_subscription = __random_subscription(SUBSCRIBER, "topic")
        subscriptions.append(random_subscription)

    network_flows = network_flow_algorithm.apply(
        firedex_configuration = firedex_configuration,
        subscriber = SUBSCRIBER,
        host = HOST,
        subscriber_subscriptions = subscriptions
    )

    mean = numpy.mean( [ subscription.utility_function() for subscription in subscriptions ] )
    variance = numpy.var( [ subscription.utility_function() for subscription in subscriptions ] )

    intra_variance = 0
    for network_flow in network_flows:
        weight = float( network_flow.subscriptions().__len__() ) / float( subscriptions.__len__() )
        current_variance = numpy.var( [ subscription.utility_function() for subscription in network_flow.subscriptions() ] )
        intra_variance += weight * current_variance

    inter_variance = 0
    for network_flow in network_flows:
        weight = float( network_flow.subscriptions().__len__() ) / float( subscriptions.__len__() )
        current_mean = numpy.mean( [ subscription.utility_function() for subscription in network_flow.subscriptions() ] )
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

if __name__ == "__main__":
    for network_flow_algorithm in NETWORK_FLOW_ALGORITHMS:
        print("algorithm: %s" % network_flow_algorithm)

        CURRENT_NETWORK_FLOW_ALGORITHM = network_flow_algorithm

        for current_network_flows in NETWORK_FLOWS:
            print("network flows: %d" % current_network_flows)

            CURRENT_NETWORK_FLOWS = current_network_flows

            for t in range(COUNT):
                print("Experiment: %d" % t)

                start = int(round(time.time() * 1000))

                for i in range(EXPERIMENTS):
                    run_experiment()

                end = int(round(time.time() * 1000))

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

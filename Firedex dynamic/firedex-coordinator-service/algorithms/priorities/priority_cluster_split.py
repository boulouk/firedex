
import random
from netrc import netrc


class PriorityClusterSplit:

    def __init__(self):
        pass

    def apply(self, firedex_configuration, network_flows):
        priorities = range( 1, 1 + firedex_configuration.priorities() )

        random_network_flows = random.sample( population = network_flows, k = priorities.__len__() )

        centroids = []

        ut = []
        for network_flow in network_flows:
            ut.append(network_flow.adjusted_utility_function())

        for random_network_flow in random_network_flows:
            adjusted_utility_function = random_network_flow.adjusted_utility_function()
            centroids.append(adjusted_utility_function)

        should_continue = True

        while should_continue:
            new_centroids = []

            for centroid in centroids:
                network_flows_by_centroid = self.__network_flows_by_centroid(
                    network_flows = network_flows,
                    centroids = centroids,
                    centroid = centroid
                )

                new_centroid = float( sum(x.adjusted_utility_function() for x in network_flows_by_centroid) ) / float( network_flows_by_centroid.__len__() )
                new_centroids.append(new_centroid)

            if new_centroids == centroids:
                should_continue = False

            centroids = new_centroids

        centroids.sort(reverse = True)

        for priority, centroid in zip(priorities, centroids):
            network_flows_by_centroid = self.__network_flows_by_centroid(
                network_flows = network_flows,
                centroids = centroids,
                centroid = centroid
            )

            for network_flow_by_centroid in network_flows_by_centroid:
                network_flow_by_centroid.set_priority(priority = priority)

    def __network_flows_by_centroid(self, network_flows, centroids, centroid):
        network_flows_by_centroid = []

        for network_flow in network_flows:
            network_flow_centroid = self.__network_flow_centroid(
                network_flow = network_flow,
                centroids = centroids
            )

            if network_flow_centroid == centroid:
                network_flows_by_centroid.append(network_flow)

        return network_flows_by_centroid

    def __network_flow_centroid(self, network_flow, centroids):
        centroid = min( centroids, key = lambda x: abs( network_flow.adjusted_utility_function() - x )  )
        return centroid


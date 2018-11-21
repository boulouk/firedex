
class FiredexConfiguration:

    def __init__(self, network_flows, priorities, network_flow_algorithm, priority_algorithm, drop_rate_algorithm, rho_tolerance):
        self.__network_flows = network_flows
        self.__priorities = priorities

        self.__network_flow_algorithm = network_flow_algorithm
        self.__priority_algorithm = priority_algorithm
        self.__drop_rate_algorithm = drop_rate_algorithm

        self.__rho_tolerance = rho_tolerance

    def network_flows(self):
        return self.__network_flows

    def priorities(self):
        return self.__priorities

    def network_flow_algorithm(self):
        return self.__network_flow_algorithm

    def priority_algorithm(self):
        return self.__priority_algorithm

    def drop_rate_algorithm(self):
        return self.__drop_rate_algorithm

    def rho_tolerance(self):
        return self.__rho_tolerance

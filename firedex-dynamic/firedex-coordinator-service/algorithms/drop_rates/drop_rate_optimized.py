
import cvxpy

class DropRateOptimized:

    def __init__(self):
        pass

    def apply(self, network_configuration, firedex_configuration, publishers_configuration, network_flows):
        bandwidth = network_configuration.bandwidth()
        rho_tolerance = firedex_configuration.rho_tolerance()
        publication_collection = publishers_configuration.publication_collection()

        # variable
        n = network_flows.__len__()
        # ---

        # problem to solve
        alpha = [ x.adjusted_utility_function() for x in network_flows ]
        success_rate = cvxpy.Variable(n, name = "success_rates")

        objective = cvxpy.Maximize(  cvxpy.sum( cvxpy.multiply(alpha, cvxpy.log1p(success_rate)) )  )
        # ---

        # constraint
        network_flows_load = []
        for network_flow in network_flows:
            subscriptions = network_flow.subscriptions()
            current_load = 0
            for subscription in subscriptions:
                topic = subscription.topic()
                current_load += publication_collection.publications_load_by_topic(topic = topic)

            network_flows_load.append(current_load)

        a = network_flows_load * success_rate
        network_load = cvxpy.sum( cvxpy.multiply(network_flows_load, success_rate) )
        constraints = [ network_load <= bandwidth * (1 - rho_tolerance), success_rate >= 0, success_rate <= 1 ]
        # ---

        # solution
        prob = cvxpy.Problem(objective, constraints)
        prob.solve()

        solution = success_rate.value
        solution = [ round(x, 2) for x in solution]
        # ---

        for network_flow, success_rate in zip(network_flows, solution):
            drop_rate = 1 - success_rate
            network_flow.set_drop_rate(drop_rate = drop_rate)

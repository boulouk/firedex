
import json
import os
import matplotlib.pyplot as python_plot
import pandas

file_theory = "./result/aggregate_theory.csv"
file_physical = "./result/aggregate_physical.csv"

def plot():
    has_theory = os.path.isfile(file_theory)
    has_physical = os.path.isfile(file_physical)

    network_flows = open("./result/network_flows.json").read()
    network_flows = json.loads(network_flows)

    priorities = []
    drop_rates = {}
    for network_flow in network_flows:
        priority = network_flow["priority"]
        drop_rate = network_flow["drop_rate"]

        if priority not in priorities:
            priorities.append(priority)

        if priority not in drop_rates.keys():
            drop_rates[priority] = drop_rate

    priorities = sorted(priorities)

    latencies_map = {}
    drop_rate_map = {}

    # LATENCY

    if has_theory:
        names_theory = ["subscriber", "topic", "priority", "success_rate", "latency_analytical", "latency_simulation"]
        table_theory = pandas.read_csv("./result/aggregate_theory.csv", names = names_theory)

        latencies_analytical = table_theory.groupby(["priority"])["latency_analytical"].mean()._values
        latencies_simulation = table_theory.groupby(["priority"])["latency_simulation"].mean()._values

        latencies_map["analytical"] = latencies_analytical
        latencies_map["simulation"] = latencies_simulation

    if has_physical:
        names_physical = ["subscriber", "topic", "port", "utility_function", "priority", "drop_rate", "sent", "received", "latency"]
        table_physical = pandas.read_csv("./result/aggregate_physical.csv", names = names_physical)

        latencies_physical = table_physical.groupby(["priority"])["latency"].mean()._values

        latencies_map["physical"] = latencies_physical

    legend = []
    for experiment_type, latencies in latencies_map.items():
        legend.append(experiment_type)
        python_plot.plot(priorities, latencies)

    python_plot.legend(legend, loc = 'upper left')
    python_plot.show()

    # DROP RATE

    success_rates_map = {}

    expected_success_rates = []

    for priority in priorities:
        drop_rate = drop_rates[priority]
        success_rate = 1 - drop_rate
        expected_success_rates.append(success_rate)

    success_rates_map["expected"] = expected_success_rates

    if has_theory:
        names_theory = ["subscriber", "topic", "priority", "success_rate", "latency_analytical", "latency_simulation"]
        table_theory = pandas.read_csv("./result/aggregate_theory.csv", names = names_theory)

        success_rates_theory = table_theory.groupby(["priority"])["success_rate"].mean()._values

        success_rates_map["theory"] = success_rates_theory

    if has_physical:
        names_physical = ["subscriber", "topic", "port", "utility_function", "priority", "drop_rate", "sent", "received", "latency"]
        table_physical = pandas.read_csv("./result/aggregate_physical.csv", names = names_physical)

        group_by_priority = table_physical.groupby(["priority"])

        sents = group_by_priority["sent"].sum()._values
        receiveds = group_by_priority["received"].sum()._values

        actual_success_rates = []
        for priority, sent, received in zip(priorities, sents, receiveds):
            success_rate = float(received) / float(sent)
            actual_success_rates.append(success_rate)

        success_rates_map["physical"] = actual_success_rates

    legend = []
    for experiment_type, success_rate in success_rates_map.items():
        legend.append(experiment_type)
        python_plot.plot(priorities, success_rate)

    python_plot.legend(legend, loc = 'upper left')
    python_plot.show()

if __name__ == "__main__":
    plot()

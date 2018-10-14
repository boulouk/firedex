
import matplotlib.pyplot as python_plot
import pandas

def plot():
    names_analytical = ["subscriber", "topic", "port", "utility_function", "priority", "drop_rate", "latency"]
    table_analytical = pandas.read_csv("./result/aggregate_analytical.csv", names = names_analytical)

    latencies_analytical = table_analytical.groupby(["priority"])["latency"].mean()._values

    names_simulation = ["subscriber", "topic", "port", "utility_function", "priority", "drop_rate", "latency"]
    table_simulation = pandas.read_csv("./result/aggregate_simulation.csv", names = names_simulation)

    latencies_simulation = table_simulation.groupby(["priority"])["latency"].mean()._values

    names_physical = ["subscriber", "topic", "port", "utility_function", "priority", "drop_rate", "sent", "received", "latency"]
    table_physical = pandas.read_csv("./result/aggregate_physical.csv", names = names_physical)

    latencies_physical = table_physical.groupby(["priority"])["latency"].mean()._values

    priorities = table_physical.priority.unique().__len__()
    priorities = range(priorities)

    python_plot.plot(priorities, latencies_analytical)
    python_plot.plot(priorities, latencies_simulation)
    python_plot.plot(priorities, latencies_physical)

    python_plot.legend(["analytical", "simulation", "physical"], loc = 'upper left')

    python_plot.show()

    table = pandas.read_csv("./result/aggregate_physical.csv", names = names)
    group_by_priority = table.groupby(["priority"])

    sents = group_by_priority["sent"].sum()._values
    receiveds = group_by_priority["received"].sum()._values

    for i, sent, received in zip( range(1, 8), sents, receiveds):
        p = float(received) / float(sent)
        print( str(i) + " -> " + str(p))

if __name__ == "__main__":
    plot()

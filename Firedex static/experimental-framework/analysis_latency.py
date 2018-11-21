
import collections
import os
import matplotlib.pyplot as python_plot
import pandas

file_to_analyze = "./result/log/sub5_log.log"

def plot():
    file_exists = os.path.isfile(file_to_analyze)

    if file_exists:
        columns = ["topic", "port", "publisher", "identifier", "sent", "received"]
        table = pandas.read_csv(file_to_analyze, names = columns)

        topic_list = table["topic"]._values
        sent_list = table["sent"]._values
        received_list = table["received"]._values

        latencies = { }

        for topic, sent, received in zip(topic_list, sent_list, received_list):
            if topic != "topicasf6":
                latency = received - sent
                if latency not in latencies.keys():
                    latencies[latency] = 0
                latencies[latency] = latencies[latency] + 1

        x = []
        y = []

        max_latency = -1
        max_count = -1

        for latency, count in latencies.items():
            if count > max_count:
                max_count = count
                max_latency = latency

        print(max_latency)
        print(max_count)

        ordered_latencies = collections.OrderedDict( sorted(latencies.items()) )

        for latency, count in ordered_latencies.items():
            x.append(latency)
            y.append(count)
            print( latency, count )

        python_plot.plot(x, y)
        python_plot.show()

if __name__ == "__main__":
    plot()

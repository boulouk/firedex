
import json
import os
import requests
import subprocess
import time

from scenario.experiment_scenario import *

from configuration.network_configuration import NetworkConfiguration
from configuration.topology_configuration import TopologyConfiguration
from configuration.firedex_configuration import FiredexConfiguration
from configuration.experiment_configuration import ExperimentConfiguration

from network.mininet_network import MininetNetwork

FIREDEX_MIDDLEWARE_HOST = "127.0.0.1"
FIREDEX_MIDDLEWARE_PORT = 8888
FIREDEX_BASE_API = "http://127.0.0.1:8888/api/firedex"

class Configuration:

    def __init__(self):
        self.network_configuration = None
        self.topology_configuration = None
        self.firedex_configuration = None
        self.experiment_configuration = None

configuration = Configuration()

def network_scenario():
    configuration.network_configuration = NetworkConfiguration()
    print("Network configuration loaded.")

def topology_scenario():
    configuration.topology_configuration = TopologyConfiguration()
    print("Topology configuration loaded.")

def firedex_scenario():
    configuration.firedex_configuration = FiredexConfiguration()
    print("Firedex configuration loaded.")

def experiment_scenario():
    configuration.experiment_configuration = ExperimentConfiguration(configuration.network_configuration,
                                                                     configuration.topology_configuration,
                                                                     configuration.firedex_configuration
                                                                    )
    print("Experiment configuration loaded.")

def push_network_configuration():
    url = FIREDEX_BASE_API + "/push-network-configuration/"
    body = configuration.network_configuration.json()

    response = requests.post(
        url = url,
        json = body
    )

    content = response.json()

    print("Network configuration pushed.")

def push_topology_configuration():
    url = FIREDEX_BASE_API + "/push-topology-configuration/"
    body = configuration.topology_configuration.json()

    response = requests.post(
        url = url,
        json = body
    )

    content = response.json()

    print("Topology configuration pushed.")

def push_firedex_configuration():
    url = FIREDEX_BASE_API + "/push-firedex-configuration/"
    body = configuration.firedex_configuration.json()

    response = requests.post(
        url = url,
        json = body
    )

    content = response.json()

    print("Firedex configuration pushed.")

def push_experiment_configuration():
    url = FIREDEX_BASE_API + "/push-experiment-configuration/"
    body = configuration.experiment_configuration.json()

    response = requests.post(
        url = url,
        json = body
    )

    content = response.json()

    print("Experiment configuration pushed.")

def apply_experiment_configuration():
    url = FIREDEX_BASE_API + "/apply-experiment-configuration/"
    body = configuration.experiment_configuration.json()

    response = requests.post(
        url = url,
        json = body
    )

    content = response.json()
    network_flows_file = open("./result/network_flows.json", "w")
    network_flows_file.write( json.dumps(content, indent = 4) )
    network_flows_file.close()

    print("Experiment configuration applied on the FireDeX middleware.")

UDP_OVERHEAD = 42
MQTT_SN_OVERHEAD = 7

def theory_experiment():
    print("--- THEORY EXPERIMENT ---")

    grouped_topics = configuration.experiment_configuration.topics()

    topics = []
    for topic_type, topics_by_type in grouped_topics.items():
        for topic in topics_by_type:
            topics.append(topic)

    publishers = configuration.experiment_configuration.publishers()
    subscribers = configuration.experiment_configuration.subscribers()

    publication_rate_by_topic = {}
    message_size_by_topic = {}

    for publisher in publishers:
        publisher = publisher["publisher"]
        publications = publisher["publications"]
        for publication in publications:
            topic = publication["topic"]
            rate = publication["rate"]
            message_size = publication["messageSize"] + UDP_OVERHEAD + MQTT_SN_OVERHEAD

            if topic not in publication_rate_by_topic and topic not in message_size_by_topic:
                publication_rate_by_topic[topic] = 0
                message_size_by_topic[topic] = 0

            publication_rate_by_topic[topic] = publication_rate_by_topic[topic] + rate
            message_size_by_topic[topic] = message_size_by_topic[topic] + (rate * message_size)

    for topic, message_size in message_size_by_topic.items():
        message_size = message_size / publication_rate_by_topic[topic]
        message_size_by_topic[topic] = message_size

    bandwidth = configuration.network_configuration.bandwidth()
    bandwidth = bandwidth / subscribers.__len__()

    lambdas = []
    mus = []

    for topic in topics:
        lambdas.append( float(publication_rate_by_topic[topic]) )
        mus.append( float(bandwidth) / float(message_size_by_topic[topic]) )

    priorities = configuration.firedex_configuration.priorities()
    success_rate_by_priority = {}

    network_flows = open("./result/network_flows.json", "r").read()
    network_flows = json.loads(network_flows)

    for network_flow in network_flows:
        priority = network_flow["priority"]
        drop_rate = network_flow["drop_rate"]
        if priority not in success_rate_by_priority:
            success_rate_by_priority[priority] = (1 - drop_rate)

    success_rates = []
    for priority in range(1, priorities + 1):
        success_rates.append( success_rate_by_priority[priority] )

    error_rate = float( configuration.network_configuration.error_rate() )
    theory_input = {
        "duration": "30000",
        "completions": "-1",
        "broker_in_rate": "6400000",
        "broker_out_rate": "6400000",
        "sdn_in_rate": "6400000",
        "sdn_out_buffer": "2048",
        "broker_in_serv": "Det",
        "broker_out_serv": "Det",
        "sdn_in_serv": "Det",
        "sdn_out_serv": "Det",
        "error_rate": error_rate,
        "lambdas": lambdas,
        "mus": mus,
        "prio_probs": success_rates
    }

    result_file = open("./result/aggregate_theory.csv", "w")

    for subscriber in subscribers:
        subscriber = subscriber["subscriber"]
        identifier = subscriber["identifier"]

        subscriptions = []
        priorities = []

        for network_flow in network_flows:
            network_flow_identifier = network_flow["identifier"]
            if network_flow_identifier == identifier:
                network_flow_subscriptions = network_flow["subscriptions"]
                priority = network_flow["priority"]
                priority = priority - 1
                for network_flow_subscription in network_flow_subscriptions:
                    topic = network_flow_subscription["topic"]
                    topic_index = topics.index(topic)

                    subscriptions.append(topic_index)
                    priorities.append(priority)

        theory_input["subscriptions"] = subscriptions
        theory_input["priorities"] = priorities

        file = open("./theory/configuration.json", "w")
        file.write( json.dumps(theory_input, indent = 4) )
        file.close()

        jar_file = "./theory/pubsub-prio.jar"
        configuration_file = "./theory/configuration.json"
        output_file = "./theory/output_theory.json"
        command = "java -cp %s pubsubpriorities.PubsubV9Sim %s %s" % (jar_file, configuration_file, output_file)

        process = subprocess.Popen(command,
                                   shell = True,
                                   # stdin = open(os.devnull),
                                   # stdout = open(os.devnull),
                                   # stderr = open(os.devnull)
                                  )
        process.wait()

        output_theory = open(output_file, "r").read().splitlines()
        for topic_index, priority, output_theory_line in zip(subscriptions, priorities, output_theory):
            topic = topics[topic_index]

            values = output_theory_line.split(",")
            success_rate = float(values[1])
            latency_analytical = float(values[2]) * 1000
            latency_simulation = float(values[0]) * 1000

            aggregate_line = "%s, %s, %d, %f, %f, %f" % (identifier, topic, priority, success_rate, latency_analytical, latency_simulation)
            result_file.write(aggregate_line)
            result_file.write(os.linesep)

    result_file.close()
    print("Theory experiment completed.")

def start_network():
    print("Starting network...")

    broker = configuration.experiment_configuration.broker()
    publishers = configuration.experiment_configuration.publishers()
    subscribers = configuration.experiment_configuration.subscribers()

    bandwidth = configuration.network_configuration.bandwidth()
    latency = configuration.network_configuration.latency()
    error_rate = configuration.network_configuration.error_rate()

    mininet_network = MininetNetwork(
        bandwidth = bandwidth,
        latency = latency,
        error_rate = error_rate
    )

    identifier = broker["identifier"]
    host = broker["host"]

    mininet_network.add_host(identifier, host)

    for subscriber in subscribers:
        subscriber = subscriber["subscriber"]

        identifier = subscriber["identifier"]
        host = subscriber["host"]

        mininet_network.add_host(identifier, host)

    for publisher in publishers:
        publisher = publisher["publisher"]

        identifier = publisher["identifier"]
        host = publisher["host"]

        mininet_network.add_host(identifier, host)

    mininet_network.start()

    print("Network started.")

    time.sleep(3)

    print("Priority queues.")
    priorities = configuration.firedex_configuration.priorities()
    mininet_network.priority_queues(priorities)

    time.sleep(1)

    return mininet_network

def ping(network):
    print("Topology discovery...")

    time.sleep(1)

    network.topology_discovery()

    time.sleep(1)

    print("Topology discovery completed.")

def start_broker(network):
    print("Starting broker...")

    broker_configuration = configuration.experiment_configuration.broker()
    identifier = broker_configuration["identifier"]
    tcp = broker_configuration["tcp"]
    udp = broker_configuration["udp"]

    broker_configuration_file = open("./application/broker/broker.configuration", "w")
    actual_broker_configuration = ("port %d" % tcp) + os.linesep + "allow_anonymous true"
    broker_configuration_file.write(actual_broker_configuration)
    broker_configuration_file.close()

    command = "java -jar ./application/broker/Broker.jar ./application/broker/broker.configuration"
    network.execute(identifier, command)

    time.sleep(3)

    command = "java -jar ./application/gateway/Gateway.jar ./application/gateway/gateway.properties"
    network.execute(identifier, command)

    print("Broker started.")

    time.sleep(3)

def start_subscriber(network):
    print("Starting subscribers...")

    subscribers = configuration.experiment_configuration.subscribers()

    for subscriber in subscribers:
        identifier = subscriber["subscriber"]["identifier"]

        configuration_file_name = ("./application/subscriber/%s.json" % identifier)
        configuration_file = open(configuration_file_name, "w")
        configuration_file.write( json.dumps(subscriber, indent = 4) )
        configuration_file.close()

        command = ("java -jar ./application/subscriber/Subscriber.jar %s" % configuration_file_name)
        network.execute(identifier, command)

        print("Subscriber started (%s)." % identifier)

def start_publisher(network):
    print("Starting publishers...")

    publishers = configuration.experiment_configuration.publishers()

    for publisher in publishers:
        identifier = publisher["publisher"]["identifier"]

        configuration_file_name = ("./application/publisher/%s.json" % identifier)
        configuration_file = open(configuration_file_name, "w")
        configuration_file.write( json.dumps(publisher, indent = 4) )
        configuration_file.close()

        command = ("java -jar ./application/publisher/Publisher.jar %s" % configuration_file_name)
        network.execute(identifier, command)

        print("Publisher started (%s)." % identifier)

def wait():
    experiment_duration = configuration.firedex_configuration.experiment_duration()
    print("Experiment started.")

    to = experiment_duration + 100
    for i in range(1, to + 1):
        time.sleep(1)
        print(str(i) + " ---> " + str(to))

    print("Experiment completed.")

def stop_network(network):
    print("Stopping network...")

    time.sleep(1)

    network.stop()

    print("Network stopped.")

    time.sleep(1)

def __subscription_network_flow(identifier, topic):
    network_flows = open("./result/network_flows.json", "r").read()
    network_flows = json.loads(network_flows)

    for network_flow in network_flows:
        subscriber_identifier = network_flow["identifier"]
        if subscriber_identifier == identifier:
            priority = network_flow["priority"]
            drop_rate = network_flow["drop_rate"]
            subscriber_subscriptions = network_flow["subscriptions"]
            for subscriber_subscription in subscriber_subscriptions:
                subscription_topic = subscriber_subscription["topic"]
                if subscription_topic == topic:
                    utility_function = subscriber_subscription["utility_function"]
                    return utility_function, priority, drop_rate

    return None

def aggregate_result():
    table_result = open("./result/aggregate_physical.csv", "w")

    publishers = configuration.experiment_configuration.publishers()

    publications_by_topic = {}

    for publisher in publishers:
        publisher_output_file_name = publisher["output"]["outputFile"]

        publisher_result = open(publisher_output_file_name, 'r').read()
        publisher_result = json.loads(publisher_result)
        publications_result = publisher_result["publicationsResult"]

        for publication_result in publications_result:
            topic = publication_result["topic"]
            sent = publication_result["messages"]

            if topic not in publications_by_topic:
                publications_by_topic[topic] = 0

            publications_by_topic[topic] = publications_by_topic[topic] + sent

    subscribers = configuration.experiment_configuration.subscribers()

    for subscriber in subscribers:
        identifier = subscriber["subscriber"]["identifier"]
        subscriber_output_file_name = subscriber["output"]["outputFile"]

        subscriber_result = open(subscriber_output_file_name, 'r').read()
        subscriber_result = json.loads(subscriber_result)
        subscriptions_result = subscriber_result["subscriptionsResult"]

        for subscription_result in subscriptions_result:
            topic = subscription_result["topic"]
            port = subscription_result["port"]
            if topic not in publications_by_topic:
                sent = 0
            else:
                sent = publications_by_topic[topic]
            received = subscription_result["messages"]
            latency = subscription_result["latency"]

            utility_function, priority, drop_rate = __subscription_network_flow(identifier, topic)

            table_result.write( identifier + ", " + topic + ", " + str(port) + ", " + str(utility_function) +
                                ", " + str(priority) + ", " + str(drop_rate) + ", " + str(sent) + ", " +
                                str(received) + ", " + str(latency) + os.linesep)

    table_result.close()
    print("Result table created.")

def physical_experiment():
    print("--- PHYSICAL EXPERIMENT ---")
    print("")

    network = start_network()

    print("")

    ping(network)

    print("")

    start_broker(network)
    time.sleep(3)
    print("")
    start_subscriber(network)
    time.sleep(10)
    print("")
    start_publisher(network)
    time.sleep(3)
    print("")

    wait()

    print("")

    stop_network(network)

    print("")

    aggregate_result()

if __name__ == "__main__":
    network_scenario()
    topology_scenario()
    firedex_scenario()
    experiment_scenario()

    print("")

    push_network_configuration()
    push_topology_configuration()
    push_firedex_configuration()
    push_experiment_configuration()

    print("")

    apply_experiment_configuration()

    print("")

    run = RUN

    if "theory" in run:
        theory_experiment()
        print("")

    if "physical" in run:
        physical_experiment()

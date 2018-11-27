
import json
import os
import requests
import subprocess
import time

from scenario.experiment_scenario import *

from configuration.network_configuration import NetworkConfiguration
from configuration.controller_configuration import ControllerConfiguration
from configuration.firedex_configuration import FiredexConfiguration
from configuration.experiment_configuration import ExperimentConfiguration

from network.mininet_network import MininetNetwork

FIREDEX_MIDDLEWARE_HOST = "127.0.0.1"
FIREDEX_MIDDLEWARE_PORT = 8888
FIREDEX_BASE_API = "http://127.0.0.1:8888/api/firedex"

class Configuration:

    def __init__(self):
        self.network_configuration = None
        self.firedex_configuration = None
        self.controller_configuration = None
        self.experiment_configuration = None

configuration = Configuration()

def network_scenario():
    configuration.network_configuration = NetworkConfiguration()
    print("Network configuration loaded.")

def firedex_scenario():
    configuration.firedex_configuration = FiredexConfiguration()
    print("Firedex configuration loaded.")

def controller_scenario():
    configuration.controller_configuration = ControllerConfiguration()
    print("Controller configuration loaded.")

def experiment_scenario():
    configuration.experiment_configuration = ExperimentConfiguration()
    print("Experiment configuration loaded.")

def push_experiment_configuration():
    url = FIREDEX_BASE_API + "/push-experiment-configuration/"
    body = {
        "network_configuration": configuration.network_configuration.as_dictionary(),
        "firedex_configuration": configuration.firedex_configuration.as_dictionary(),
        "controller_configuration": configuration.controller_configuration.as_dictionary()
    }

    data = json.dumps(body, indent = 4)

    response = requests.post(
        url = url,
        json = data
    )

    print("Experiment configuration pushed.")

def start_network():
    print("Starting network...")

    broker = configuration.experiment_configuration.broker()
    publishers = configuration.experiment_configuration.publishers()
    subscribers = configuration.experiment_configuration.subscribers()

    bandwidth = configuration.network_configuration.bandwidth()
    delay = configuration.network_configuration.delay()
    error_rate = configuration.network_configuration.error_rate()

    mininet_network = MininetNetwork(
        bandwidth = bandwidth,
        delay = delay,
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

    command = "java -jar ./application/broker/Broker.jar ./application/broker/broker.configuration"
    network.execute(identifier, command)

    time.sleep(3)

    command = "java -jar ./application/gateway/Gateway.jar ./application/gateway/gateway.properties"
    network.execute(identifier, command)

    print("Broker started.")

    time.sleep(3)

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

def wait():
    experiment_duration = configuration.experiment_configuration.experiment_duration()
    print("Experiment started.")

    to = experiment_duration + 300
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

if __name__ == "__main__":
    network_scenario()
    firedex_scenario()
    controller_scenario()
    experiment_scenario()

    print("")

    push_experiment_configuration()

    print("")

    network = start_network()
    ping(network)

    print("")

    start_broker(network)

    print("")

    start_publisher(network)

    time.sleep(5)

    start_subscriber(network)

    print("")

    wait()

    print("")

    stop_network(network)

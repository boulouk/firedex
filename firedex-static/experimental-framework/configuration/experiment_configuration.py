
import os
import json
import random

import numpy

class ExperimentConfiguration:

    def __init__(self, network_configuration, topology_configuration, firedex_configuration):
        base_host = "10.0.0.%d"
        host_index = 1

        broker_host = (base_host % host_index)
        host_index = host_index + 1
        broker_tcp = topology_configuration.broker()["tcp"]
        broker_udp = topology_configuration.broker()["udp"]

        self.__broker = {
            "identifier": "broker",
            "host": broker_host,
            "tcp": broker_tcp,
            "udp": broker_udp
        }

        types = topology_configuration.types()

        all_topics = {}

        topic_base_name = "topic"
        topic_index = 0

        for type in types:
            all_topics[type] = []
            count = topology_configuration.topic()[type]
            for i in range(count):
                topic_name = topic_base_name + str(topic_index)
                all_topics[type].append(topic_name)
                topic_index = topic_index + 1

        self.__topics = all_topics

        subscriber_base_name = "sub"
        subscriber_index = 0

        subscriber_scenario = topology_configuration.subscriber()["scenario"]

        subscribers = []

        for subscriber_group in subscriber_scenario:
            subscriber_count = subscriber_group["count"]
            for i in range(subscriber_count):
                identifier = subscriber_base_name + str(subscriber_index)
                running_time = firedex_configuration.experiment_duration() + 100
                subscriptions = []

                for type in types:
                    subscription_count = subscriber_group[type]["count"]
                    topics = self.__sample(all_topics, type, subscription_count)
                    utility_functions = []

                    for j in range(subscription_count):
                        utility_function_average = subscriber_group[type]["utility_function"]["average"]
                        utility_function_lower_bound = subscriber_group[type]["utility_function"]["lower_bound"]
                        utility_function_upper_bound = subscriber_group[type]["utility_function"]["upper_bound"]
                        utility_functions.append(self.__random(utility_function_average,
                                                               utility_function_lower_bound,
                                                               utility_function_upper_bound
                                                              )
                                                )

                    for topic, utility_function in zip(topics, utility_functions):
                        subscriptions.append(
                            {
                                "topic": topic,
                                "utilityFunction": utility_function,
                                "time": 0
                            }
                        )

                subscriber = {
                    "server": {
                        "middleware": {
                            "host": firedex_configuration.host(),
                            "port": firedex_configuration.port()
                        },
                        "broker": {
                            "host": broker_host,
                            "port": broker_udp
                        }
                    },
                    "subscriber": {
                        "identifier": identifier,
                        "host": (base_host % host_index),
                        "runningTime": running_time,
                        "subscriptions": subscriptions
                    },
                    "output": {
                        "logFile": ("./result/log/%s_log.log" % identifier),
                        "outputFile": ("./result/output/%s_output.json" % identifier)
                    }
                }

                subscribers.append(subscriber)

                host_index = host_index + 1
                subscriber_index = subscriber_index + 1

        self.__subscribers = subscribers

        publisher_base_name = "pub"
        publisher_index = 0

        publisher_scenario = topology_configuration.publisher()["scenario"]

        publishers = []

        for publisher_group in publisher_scenario:
            publisher_count = publisher_group["count"]
            for i in range(publisher_count):
                identifier = publisher_base_name + str(publisher_index)
                running_time = firedex_configuration.experiment_duration()
                publications = []

                for type in types:
                    publication_count = publisher_group[type]["count"]
                    topics = self.__sample(all_topics, type, publication_count)
                    rates = []
                    sizes = []

                    for j in range(publication_count):
                        rate_average = publisher_group[type]["rate"]["average"]
                        rate_lower_bound = publisher_group[type]["rate"]["lower_bound"]
                        rate_upper_bound = publisher_group[type]["rate"]["upper_bound"]
                        rates.append( self.__random(rate_average, rate_lower_bound, rate_upper_bound) )

                        size_average = publisher_group[type]["size"]["average"]
                        size_lower_bound = publisher_group[type]["size"]["lower_bound"]
                        size_upper_bound = publisher_group[type]["size"]["upper_bound"]
                        size = int( self.__random(size_average, size_lower_bound, size_upper_bound) )
                        sizes.append(size)

                    for topic, rate, size in zip(topics, rates, sizes):
                        publications.append(
                            {
                                "topic": topic,
                                "rateType": type,
                                "rate": rate,
                                "messageSize": size,
                                "qualityOfService": 0,
                                "retained": False
                            }
                        )

                publisher = {
                    "broker": {
                        "host": broker_host,
                        "port": broker_tcp
                    },
                    "publisher": {
                        "identifier": identifier,
                        "host": (base_host % host_index),
                        "runningTime": running_time,
                        "publications": publications
                    },
                    "output": {
                        "logFile": ("./result/log/%s_log.log" % identifier),
                        "outputFile": ("./result/output/%s_output.json" % identifier)
                    }
                }

                publishers.append(publisher)

                host_index = host_index + 1
                publisher_index = publisher_index + 1

        self.__publishers = publishers

    def __sample(self, all_topics, type, count):
        selected_topics = random.sample(all_topics[type], count)
        return selected_topics

    def __random(self, average, lower_bound, upper_bound):
        value = numpy.random.exponential(average)
        if value < lower_bound:
            value = lower_bound
        if value > upper_bound:
            value = upper_bound

        return value

    def topics(self):
        return self.__topics

    def broker(self):
        return self.__broker

    def subscribers(self):
        return self.__subscribers

    def publishers(self):
        return self.__publishers

    def json(self):
        object = {
            "topics": self.topics(),

            "broker": self.broker(),
            "subscribers": self.subscribers(),
            "publishers": self.publishers()
        }

        result = json.dumps(object, indent = 4, sort_keys = False)
        return result

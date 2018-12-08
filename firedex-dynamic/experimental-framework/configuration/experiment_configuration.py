
import os
import json
import random

import numpy

from scenario.experiment_scenario import *

class ExperimentConfiguration:

    def __init__(self):
        self.__experiment_duration = EXPERIMENT_DURATION

        base_host = "10.0.0.%d"
        host_index = 1

        broker_host = (base_host % host_index)
        host_index = host_index + 1

        self.__broker = {
            "identifier": "broker",
            "host": broker_host
        }

        topic = TOPIC

        topic_base_name = "topic"
        topic_index = 1

        self.__topics = {}

        for topic_type, topic_count in topic.items():
            self.__topics[topic_type] = []
            for i in range(topic_count):
                topic_name = topic_base_name + str(topic_index)
                self.__topics[topic_type].append(topic_name)
                topic_index = topic_index + 1

        self.__topics["random"].append("smoke")
        self.__topics["random"].append("water_pressure")

        subscriber_base_name = "sub"
        subscriber_index = 1

        subscriber_scenario = SUBSCRIBER["scenario"]

        subscribers = []

        for subscriber_group in subscriber_scenario:
            subscriber_count = subscriber_group["count"]
            for i in range(subscriber_count):
                identifier = subscriber_base_name + str(subscriber_index)
                running_time = EXPERIMENT_DURATION + 180
                subscriptions = []

                for topic_type in self.__topics.keys():
                    subscription_count = subscriber_group[topic_type]["count"]
                    topics = self.__sample( self.__topics, topic_type, subscription_count )
                    utility_functions = []
                    times = []

                    for j in range(subscription_count):
                        utility_function_average = subscriber_group[topic_type]["utility_function"]["average"]
                        utility_function_lower_bound = subscriber_group[topic_type]["utility_function"]["lower_bound"]
                        utility_function_upper_bound = subscriber_group[topic_type]["utility_function"]["upper_bound"]
                        utility_functions.append(
                            self.__random(
                                utility_function_average,
                                utility_function_lower_bound,
                                utility_function_upper_bound
                            )
                        )

                        time_average = subscriber_group[topic_type]["time"]["average"]
                        time_lower_bound = subscriber_group[topic_type]["time"]["lower_bound"]
                        time_upper_bound = subscriber_group[topic_type]["time"]["upper_bound"]
                        times.append(
                            self.__random(
                                time_average,
                                time_lower_bound,
                                time_upper_bound
                            )
                        )

                    for topic, utility_function, time in zip(topics, utility_functions, times):
                        subscriptions.append(
                            {
                                "topic": topic,
                                "utilityFunction": utility_function,
                                "time": time
                            }
                        )

                subscriber = {
                    "server": {
                        "middleware": {
                            "host": HOST,
                            "port": PORT
                        },
                        "broker": {
                            "host": broker_host,
                            "port": 20000
                        },
                        "web": {
                            "abilitate": True,
                            "port": 5000
                        }
                    },
                    "subscriber": {
                        "identifier": identifier,
                        "host": (base_host % host_index),
                        "runningTime": running_time,
                        "startAfter": 0,
                        "subscriptions": subscriptions,
                        "modifications": [],
                        "unsubscriptions": []
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
        publisher_index = 1

        publisher_scenario = PUBLISHER["scenario"]

        publishers = []

        for publisher_group in publisher_scenario:
            publisher_count = publisher_group["count"]
            for i in range(publisher_count):
                identifier = publisher_base_name + str(publisher_index)
                running_time = EXPERIMENT_DURATION
                publications = []

                for topic_type in self.__topics.keys():
                    publication_count = publisher_group[topic_type]["count"]
                    topics = self.__sample(self.__topics, topic_type, publication_count)
                    rates = []
                    sizes = []

                    for j in range(publication_count):
                        rate_average = publisher_group[topic_type]["rate"]["average"]
                        rate_lower_bound = publisher_group[topic_type]["rate"]["lower_bound"]
                        rate_upper_bound = publisher_group[topic_type]["rate"]["upper_bound"]
                        rates.append( self.__random(rate_average, rate_lower_bound, rate_upper_bound) )

                        size_average = publisher_group[topic_type]["size"]["average"]
                        size_lower_bound = publisher_group[topic_type]["size"]["lower_bound"]
                        size_upper_bound = publisher_group[topic_type]["size"]["upper_bound"]
                        size = int( self.__random(size_average, size_lower_bound, size_upper_bound) )
                        sizes.append(size)

                    for topic, rate, size in zip(topics, rates, sizes):
                        publications.append(
                            {
                                "topic": topic,
                                "rateType": topic_type,
                                "rate": rate,
                                "messageSize": size,
                                "qualityOfService": 0,
                                "retained": False
                            }
                        )

                publisher = {
                    "server": {
                        "middleware": {
                            "host": HOST,
                            "port": PORT
                        },
                        "broker": {
                            "host": broker_host,
                            "port": 1883
                        }
                    },
                    "publisher": {
                        "identifier": identifier,
                        "host": (base_host % host_index),
                        "runningTime": running_time,
                        "startAfter": 60,
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

    def __sample(self, topics, topic_type, count):
        selected_topics = random.sample(topics[topic_type], count)
        return selected_topics

    def __random(self, average, lower_bound, upper_bound):
        value = numpy.random.exponential(average)
        if value < lower_bound:
            value = lower_bound
        if value > upper_bound:
            value = upper_bound

        return value

    def experiment_duration(self):
        return self.__experiment_duration

    def topics(self):
        return self.__topics

    def broker(self):
        return self.__broker

    def subscribers(self):
        return self.__subscribers

    def publishers(self):
        return self.__publishers

    def as_dictionary(self):
        object = {
            "experiment_duration": self.experiment_duration(),

            "topics": self.topics(),

            "broker": self.broker(),
            "subscribers": self.subscribers(),
            "publishers": self.publishers()
        }

        return object

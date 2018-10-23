
BROKER = {
    "tcp": 1883,
    "udp": 20000
}

TYPES = [ "deterministic", "random" ]

TOPICS = 7
TOPIC = {
    "deterministic": 0,
    "random": 7
}

SUBSCRIBERS = 10
SUBSCRIBER = {
    "scenario": [
        {
            "count": 10,
            "deterministic": {
                "count": 0,
                "utility_function": { "average": 5, "lower_bound": 0.01, "upper_bound": 100 }
            },
            "random": {
                "count": 7,
                "utility_function": { "average": 5, "lower_bound": 0.01, "upper_bound": 100 }
            }
        }
    ]
}

PUBLISHERS = 1
PUBLISHER = {
    "scenario": [
        {
            "count": 1,

            "deterministic": {
                "count": 0,
                "rate": { "average": 10, "lower_bound": 10, "upper_bound": 10 },
                "size": { "average": 51, "lower_bound": 51, "upper_bound": 51 }
            },
            "random": {
                "count": 7,
                "rate": { "average": 10, "lower_bound": 10, "upper_bound": 10 },
                "size": { "average": 51, "lower_bound": 51, "upper_bound": 51 }
            }
        }
    ]

}

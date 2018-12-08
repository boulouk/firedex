
HOST = "10.0.2.15"
PORT = "8888"

EXPERIMENT_DURATION = 10800

TOPIC = {
    "deterministic": 0,
    "random": 4
}

SUBSCRIBER = {
    "scenario": [
        {
            "count": 4,

            "deterministic": {
                "count": 0,
                "utility_function": { "average": 7.5, "lower_bound": 5, "upper_bound": 10 },
                "time": { "average": 0, "lower_bound": 0, "upper_bound": 0 }
            },

            "random": {
                "count": 6,
                "utility_function": { "average": 7.5, "lower_bound": 5, "upper_bound": 10 },
                "time": { "average": 0, "lower_bound": 0, "upper_bound": 0 }
            }
        },
        {
            "count": 1,

            "deterministic": {
                "count": 0,
                "utility_function": { "average": 7.5, "lower_bound": 5, "upper_bound": 10 },
                "time": { "average": 0, "lower_bound": 0, "upper_bound": 0 }
            },

            "random": {
                "count": 0,
                "utility_function": { "average": 7.5, "lower_bound": 5, "upper_bound": 10 },
                "time": { "average": 0, "lower_bound": 0, "upper_bound": 0 }
            }
        }
    ]
}

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
                "count": 6,
                "rate": { "average": 10, "lower_bound": 10, "upper_bound": 10 },
                "size": { "average": 51, "lower_bound": 51, "upper_bound": 51 }
            }
        }
    ]

}


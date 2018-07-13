
import random

from flask import Flask, jsonify


application = Flask("firedex-middleware")

__priorities = [
    {"priority": "0", "port": "10000" },
    {"priority": "1", "port": "10001" },
    {"priority": "2", "port": "10002" },
    {"priority": "3", "port": "10003" }
]

@application.route("/api/firedex/priorities", methods = ["GET"])
def priorities():
    return jsonify( __priorities )

@application.route("/api/firedex/<string:topic>/<int:utility_function>", methods = ["GET"])
def priority(topic, utility_function):
    n = __priorities.__len__()

    index = random.randint(0, n - 1)
    __priority = __priorities[index]

    response = {
        "topic": topic,
        "utility_function": utility_function,
        "priority": __priority["priority"],
        "port": __priority["port"]
    }
    return jsonify(response)


if __name__ == "__main__":
    application.run(debug = True)

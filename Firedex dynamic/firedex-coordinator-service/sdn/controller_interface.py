
import json
import requests

class ControllerInterface:

    def __init__(self, host, port, switch_identifier):
        self.__host = host
        self.__port = port
        self.__switch_identifier = switch_identifier

    def add_firedex_policies(self, network_flows):
        url = "http://%s:%d/api/flow/add-firedex-policies/" % (self.__host, self.__port)
        self.__firedex_policies(
            url = url,
            network_flows = network_flows
        )

    def modify_firedex_policies(self, network_flows):
        url = "http://%s:%d/api/flow/modify-firedex-policies/" % (self.__host, self.__port)
        self.__firedex_policies(
            url = url,
            network_flows = network_flows
        )

    def remove_firedex_policies(self, network_flows):
        url = "http://%s:%d/api/flow/remove-firedex-policies/" % (self.__host, self.__port)
        self.__firedex_policies(
            url = url,
            network_flows = network_flows
        )

    def __firedex_policies(self, url, network_flows):
        network_flow_data = {
            "switch_identifier": self.__switch_identifier,
            "policies": []
        }

        for network_flow in network_flows:
            policy = {
                "destination_ip_address": network_flow.host(),
                "destination_transport_port": network_flow.port(),
                "priority": network_flow.get_priority(),
                "drop_rate": network_flow.get_drop_rate()
            }
            network_flow_data["policies"].append(policy)

        data = json.dumps(network_flow_data)
        requests.post(url, data = data)

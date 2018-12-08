
import networkx as nx

class TopologyManager:

    def __init__(self):
        self.__graph = nx.Graph()

    # TOPOLOGY API

    def add_switch(self, switch_identifier):
        if self.exists_switch(switch_identifier = switch_identifier):
            return False

        description = {
            "type": "switch"
        }

        self.__graph.add_node(
            n = switch_identifier,
            description = description
        )

        return True

    def remove_switch(self, switch_identifier):
        if not self.exists_switch(switch_identifier = switch_identifier):
            return False

        self.__graph.remove_node(n = switch_identifier)

        for host in self.hosts(): # removes all the hosts connected to the switch
            host_description = self.__graph.node[host]["description"]
            switch_identifier_connected_to = host_description["switch_identifier_connected_to"]
            if switch_identifier_connected_to == switch_identifier:
                self.__graph.remove_node(n = host)

        return True

    def switches(self):
        switches = []

        for node in self.__graph.nodes(data ="description"):
            node_identifier = node[0]
            node_type = node[1]["type"]
            if node_type == "switch":
                switches.append(node_identifier)

        return switches

    def add_host(self, host_identifier):
        if self.exists_host(host_identifier = host_identifier):
            return False

        description = {
            "type": "host"
        }

        self.__graph.add_node(
            n = host_identifier,
            description = description
        )

        return True

    def update_host(self, host_identifier, **host_parameters):
        if not self.exists_host(host_identifier = host_identifier):
            return False

        for parameter, parameter_value in host_parameters.items():
            self.__graph.node[host_identifier]["description"][parameter] = parameter_value

        return True

    def remove_host(self, host_identifier):
        if not self.exists_host(host_identifier = host_identifier):
            return False

        self.__graph.remove_node(n = host_identifier)
        return True

    def hosts(self):
        hosts = []

        for node in self.__graph.nodes(data ="description"):
            node_identifier = node[0]
            node_type = node[1]["type"]
            if node_type == "host":
                hosts.append(node_identifier)

        return hosts

    def add_link(self, node_from_identifier, node_to_identifier, node_from_port, node_to_port):
        if not self.__graph.has_node(n = node_from_identifier) or not self.__graph.has_node(n = node_to_identifier):
            return False

        if self.exists_link(node_from_identifier = node_from_identifier, node_to_identifier = node_to_identifier):
            return False

        description = {
            "type": "link",
            str(node_from_identifier): node_from_port,
            str(node_to_identifier): node_to_port
        }

        self.__graph.add_edge(
            u = node_from_identifier,
            v = node_to_identifier,
            description = description
        )

        return True

    def remove_link(self, node_from_identifier, node_to_identifier):
        if not self.__graph.has_node(n = node_from_identifier) or not self.__graph.has_node(n = node_to_identifier):
            return False

        if not self.exists_link(node_from_identifier = node_from_identifier, node_to_identifier = node_to_identifier):
            return False

        self.__graph.remove_edge(
            u = node_from_identifier,
            v = node_to_identifier
        )

        return True

    def links(self):
        edges = []

        for edge in self.__graph.edges():
            edges.append(edge)

        return edges

    def exists_switch(self, switch_identifier):
        exists = self.switches().__contains__(switch_identifier)
        return exists

    def exists_host(self, host_identifier):
        exists = self.hosts().__contains__(host_identifier)
        return exists

    def exists_link(self, node_from_identifier, node_to_identifier):
        exists = self.__graph.has_edge(
            u = node_from_identifier,
            v = node_to_identifier
        )

        return exists

    def clear_topology(self):
        self.__graph.clear()

    # ---

    # REST API

    def topology(self):
        topology = {
            "nodes": {
                "switches": self.switches(),
                "hosts": self.hosts()
            },
            "links": self.links()
        }

        return topology

    def output_port_to_mac_address(self, source_identifier, destination_mac_address):
        if not self.__graph.has_node(n = source_identifier) or not self.__graph.has_node(n = destination_mac_address):
            return "None"

        shortest_path = nx.shortest_path(
            G = self.__graph,
            source = source_identifier,
            target = destination_mac_address
        )

        current_hop = shortest_path[0]
        next_hop = shortest_path[1]

        edge_data = self.__graph.get_edge_data(
            u = current_hop,
            v = next_hop
        )

        output_port = edge_data["description"][current_hop]
        return output_port

    def output_port_to_ip_address(self, source_identifier, destination_ip_address):
        for node in self.__graph.nodes(data = "description"):
            node_identifier = node[0]
            node_type = node[1]["type"]
            if node_type == "host":
                node_ip_address = node[1]["ip_address"]
                if node_ip_address == destination_ip_address:
                    output_port = self.output_port_to_mac_address(
                        source_identifier = source_identifier,
                        destination_mac_address = node_identifier
                    )
                    return output_port

        return "None"

    # ---

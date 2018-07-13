
import networkx as nx


class TopologyManager:

    def __init__(self):
        self.topology = nx.Graph()

    def add_switch(self, switch_identifier):
        if self.exists_switch(switch_identifier):
            return False

        description = {
            "type": "switch"
        }

        self.topology.add_node( switch_identifier, description = description )
        return True

    def remove_switch(self, switch_identifier):
        if not self.exists_switch(switch_identifier):
            return False

        self.topology.remove_node(switch_identifier)

        for host in self.hosts():
            host_description = self.topology.node[host]["description"]
            switch_identifier_connected_to = host_description["switch_identifier_connected_to"]
            if switch_identifier_connected_to == switch_identifier:
                self.topology.remove_node(host)

        return True

    def switches(self):
        switches = []

        for node in self.topology.nodes(data = "description"):
            node_identifier = node[0]
            node_type = node[1]["type"]
            if node_type == "switch":
                switches.append(node_identifier)

        return switches

    def add_host(self, host_identifier):
        if self.exists_host(host_identifier):
            return False

        description = {
            "type": "host"
        }

        self.topology.add_node(host_identifier, description = description)
        return True

    def remove_host(self, host_identifier):
        if not self.exists_host(host_identifier):
            return False

        self.topology.remove_node(host_identifier)
        return True

    def update_host(self, host_identifier, **host_parameters):
        if not self.exists_host(host_identifier):
            return False

        for parameter, parameter_value in host_parameters.items():
            self.topology.node[host_identifier]["description"][parameter] = parameter_value

        return True

    def hosts(self):
        hosts = []

        for node in self.topology.nodes(data = "description"):
            node_identifier = node[0]
            node_type = node[1]["type"]
            if node_type == "host":
                hosts.append(node_identifier)

        return hosts

    def add_link(self, node_from_identifier, node_to_identifier, node_from_port, node_to_port):
        if not self.topology.has_node(node_from_identifier) or not self.topology.has_node(node_to_identifier):
            return False

        if self.exists_link(node_from_identifier, node_to_identifier):
            return False

        description = {
            "type": "link",
            ("port_" + node_from_identifier): node_from_port,
            ("port_" + node_to_identifier): node_to_port
        }

        self.topology.add_edge(node_from_identifier, node_to_identifier, description = description)
        return True

    def remove_link(self, node_from_identifier, node_to_identifier):
        if not self.topology.has_node(node_from_identifier) or not self.topology.has_node(node_to_identifier):
            return False

        if not self.exists_link(node_from_identifier, node_to_identifier):
            return False

        self.topology.remove_edge(node_from_identifier, node_to_identifier)
        return True

    def exists_switch(self, switch_identifier):
        exists = self.switches().__contains__(switch_identifier)
        return exists

    def exists_host(self, host_identifier):
        exists = self.hosts().__contains__(host_identifier)
        return exists

    def exists_link(self, node_identifier_from, node_identifier_to):
        exists = self.topology.has_edge(node_identifier_from, node_identifier_to)
        return exists

    def clear_topology(self):
        self.topology.clear()

    def output_port(self, source_identifier, destination_identifier):
        if not self.topology.has_node(source_identifier) or not self.topology.has_node(destination_identifier):
            return "None"

        shortest_path = nx.shortest_path(self.topology, source_identifier, destination_identifier)

        current_hop = shortest_path[0]
        next_hop = shortest_path[1]
        description = self.topology.get_edge_data(current_hop, next_hop)
        output_port = description["description"]["port_" + current_hop]

        return output_port

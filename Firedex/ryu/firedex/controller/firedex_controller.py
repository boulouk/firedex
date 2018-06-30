
import networkx as nx

class FiredexController:

    def __init__(self):
        # Topology variables
        self.topology = nx.Graph()
        self.from_switch_identifier_to_switch_datapath = { }
        # ---

        # Flow variables
        self.from_flow_type_to_flow_rule_priority = { "ARP": 1, "ICMP": 2, "UDP": 3, "TCP": 4}
        # ---

    # Topology methods

    def add_switch(self, switch_identifier, switch_datapath):
        if self.exists_switch(switch_identifier):
            return False

        switch_description = {
            "type": "switch"
        }

        self.topology.add_node(switch_identifier, description = switch_description)
        self.from_switch_identifier_to_switch_datapath[switch_identifier] = switch_datapath
        return True

    def remove_switch(self, switch_identifier):
        if not self.topology.has_node(switch_identifier):
            return False

        self.topology.remove_node(switch_identifier)
        del self.from_switch_identifier_to_switch_datapath[switch_identifier]
        return True

    def add_host(self, host_identifier, host_mac_address, host_ip_address):
        if self.exists_host(host_identifier):
            return False

        host_description = {
            "type": "host",
            "mac_address": host_mac_address,
            "ip_address": host_ip_address
        }

        self.topology.add_node(host_identifier, description = host_description)
        return True

    def remove_host(self, host_identifier):
        if not self.topology.has_node(host_identifier):
            return False

        self.topology.remove_node(host_identifier)
        return True

    def add_link(self, node_identifier_1, node_identifier_2, node_port_1, node_port_2):
        if self.exists_link(node_identifier_1, node_identifier_2):
            return False

        link_description = {
            "type": "link",
            ("port_" + node_identifier_1): node_port_1,
            ("port_" + node_identifier_2): node_port_2
        }

        self.topology.add_edge(node_identifier_1, node_identifier_2, description = link_description)
        return True

    def remove_link(self, node_identifier_1, node_identifier_2,):
        if not self.topology.has_edge(node_identifier_1, node_identifier_2):
            return False

        self.topology.remove_edge(node_identifier_1, node_identifier_2)
        return True

    def exists_switch(self, switch_identifier):
        exists = self.topology.has_node(switch_identifier)
        return exists

    def exists_host(self, host_identifier):
        exists = self.topology.has_node(host_identifier)
        return exists

    def exists_link(self, node_identifier_1, node_identifier_2):
        exists = self.topology.has_edge(node_identifier_1, node_identifier_2)
        return exists

    def shortest_path(self, source_switch_identifier, destination_ip_address):
        source = source_switch_identifier
        destination = self.get_host_identifier_by_ip_address(destination_ip_address)

        if destination is None:
            return None

        path = nx.shortest_path(self.topology, source, destination)
        return path

    def output_port(self, shortest_path):
        current_hop = shortest_path[0]
        next_hop = shortest_path[1]
        description = self.topology.get_edge_data(current_hop, next_hop)
        output_port = description["description"]["port_" + current_hop]

        return output_port

    def clear_topology(self):
        self.topology.clear()
        self.from_switch_identifier_to_switch_datapath.clear()

    # ---

    # Flow methods

    def add_flow_rule(self, switch_identifier, priority, match, actions):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        instructions = [ parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions) ]
        flow_modification = parser.OFPFlowMod(datapath = switch_datapath, priority = priority, match = match, instructions = instructions)

        switch_datapath.send_msg(flow_modification)

    def build_priority(self, flow_type):
        flow_type = flow_type.upper()
        flow_rule_priority = self.from_flow_type_to_flow_rule_priority[flow_type]
        return flow_rule_priority

    def build_match_arp(self, switch_identifier, input_port, dl_type, dl_src, dl_dst):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser
        match = parser.OFPMatch(in_port = input_port, eth_type = dl_type, eth_src = dl_src, eth_dst = dl_dst)
        return match

    def build_match_icmp(self, switch_identifier, input_port, dl_type, nw_protocol, nw_src, nw_dst):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser
        match = parser.OFPMatch(in_port = input_port, eth_type = dl_type, ip_proto = nw_protocol, ipv4_src = nw_src, ipv4_dst = nw_dst)
        return match

    def build_actions(self, switch_identifier, output_port):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser
        actions = [ parser.OFPActionOutput(output_port) ]
        return actions

    # ---

    # Utility methods

    def get_host_identifier_by_mac_address(self, mac_address_to_find):
        for node in self.topology.nodes(data = True):
            identifier = node[0]
            description = node[1]
            node_type = description["type"]
            if node_type == "host":
                mac_address = description["mac_address"]
                if mac_address == mac_address_to_find:
                    return identifier

        return None

    def get_host_identifier_by_ip_address(self, ip_address_to_find):
        default = { "mac_address": "00:00:00:00:00:00", "ip_address": "0.0.0.0" }
        for node in self.topology.nodes(data = "description", default = default):
            identifier = node[0]
            description = node[1]
            node_type = description["type"]
            if node_type == "host":
                ip_address = description["ip_address"]
                if ip_address == ip_address_to_find:
                    return identifier

        return None

    # ---

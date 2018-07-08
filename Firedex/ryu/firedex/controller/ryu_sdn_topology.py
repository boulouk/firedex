
import networkx as nx

from ryu.lib.packet import ether_types
from ryu.lib.packet import in_proto
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto.ofproto_v1_3_parser import OFPAction
from ryu.ofproto.ofproto_v1_3_parser import OFPBucket
from ryu.ofproto.ofproto_v1_3_parser import OFPMatch


class RyuSdnTopology:

    def __init__(self):
        # Topology variables
        self.topology = nx.Graph()
        self.from_switch_identifier_to_switch_datapath = { }
        # ---

        # Flow variables
        self.from_packet_type_to_flow_rule_priority = { "ARP": 1, "ICMP": 2, "UDP": 3, "TCP": 4 }
        self.available_actions = [ "DROP", "SET-QUEUE", "OUTPUT", "GROUP" ]
        self.from_group_type_to_group_type_identifier = {
                                                          "ALL": ofproto_v1_3.OFPGT_ALL,
                                                          "SELECT": ofproto_v1_3.OFPGT_SELECT,
                                                          "INDIRECT": ofproto_v1_3.OFPGT_INDIRECT,
                                                          "FAST-FAILURE": ofproto_v1_3.OFPGT_FF
                                                        }
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

    def exists_switch(self, switch_identifier):
        exists = self.topology.has_node(switch_identifier)
        return exists

    def exists_host(self, host_identifier):
        exists = self.topology.has_node(host_identifier)
        return exists

    def exists_link(self, node_identifier_1, node_identifier_2):
        exists = self.topology.has_edge(node_identifier_1, node_identifier_2)
        return exists

    def clear_topology(self):
        self.topology.clear()
        self.from_switch_identifier_to_switch_datapath.clear()

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

    # ---

    # Flow methods

    def build_flow_rule(self, switch_identifier, priority, match, actions, idle_timeout = 0, hard_timeout = 0):
        # PRE-CONDITIONS
        self.check_switch_identifier(switch_identifier)
        self.check_priority(priority)
        self.check_match(match)
        self.check_actions(actions)
        self.check_idle_timeout(idle_timeout)
        self.check_hard_timeout(hard_timeout)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        instructions = [ parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions) ]
        flow_modification = parser.OFPFlowMod(
                                               datapath = switch_datapath,
                                               priority = priority,
                                               match = match,
                                               instructions = instructions,
                                               idle_timeout = idle_timeout,
                                               hard_timeout = hard_timeout
                                             )

        switch_datapath.send_msg(flow_modification)

    def build_priority(self, packet_type):
        packet_type = packet_type.upper()

        # PRE-CONDITIONS
        self.check_packet_type(packet_type)
        # ---

        flow_rule_priority = self.from_packet_type_to_flow_rule_priority[packet_type]
        return flow_rule_priority

    def build_match(self, switch_identifier, packet_type, input_port, match_parameters):
        packet_type = packet_type.upper()

        # PRE-CONDITIONS
        self.check_switch_identifier(switch_identifier)
        self.check_packet_type(packet_type)
        self.check_input_port(input_port)
        # match_parameters: check delegated to the specific match methods
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        if packet_type == "ARP":
            match = self.__build_match_arp(switch_identifier, input_port, match_parameters)
            return match
        elif packet_type == "ICMP":
            match = self.__build_match_icmp(switch_identifier, input_port, match_parameters)
            return match
        elif packet_type == "UDP":
            match = self.__build_match_udp(switch_identifier, input_port, match_parameters)
            return match
        elif packet_type == "TCP":
            match = self.__build_match_tcp(switch_identifier, input_port, match_parameters)
            return match

        # should not reach this line

    def __build_match_arp(self, switch_identifier, input_port, match_parameters):
        # PRE-CONDITIONS
        # switch_identifier: check delegated to the calling method
        # input_port: check delegated to the calling method
        self.check_match_parameters_arp(match_parameters)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        dl_type = ether_types.ETH_TYPE_ARP

        match = parser.OFPMatch(
                                 in_port = input_port,
                                 eth_type = dl_type,
                                 ** match_parameters
                               )
        return match

    def __build_match_icmp(self, switch_identifier, input_port, match_parameters):
        # PRE-CONDITIONS
        # switch_identifier: check delegated to the calling method
        # input_port: check delegated to the calling method
        self.check_match_parameters_icmp(match_parameters)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        dl_type = ether_types.ETH_TYPE_IP
        nw_protocol = in_proto.IPPROTO_ICMP

        match = parser.OFPMatch(
                                 in_port = input_port,
                                 eth_type = dl_type,
                                 ip_proto = nw_protocol,
                                 ** match_parameters
                               )
        return match

    def __build_match_udp(self, switch_identifier, input_port, match_parameters):
        # PRE-CONDITIONS
        # switch_identifier: check delegated to the calling method
        # input_port: check delegated to the calling method
        self.check_match_parameters_udp(match_parameters)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        dl_type = ether_types.ETH_TYPE_IP
        nw_protocol = in_proto.IPPROTO_UDP

        match = parser.OFPMatch(
                                 in_port = input_port,
                                 eth_type = dl_type,
                                 ip_proto = nw_protocol,
                                 ** match_parameters
                               )
        return match

    def __build_match_tcp(self, switch_identifier, input_port, match_parameters):
        # PRE-CONDITIONS
        # switch_identifier: check delegated to the calling method
        # input_port: check delegated to the calling method
        self.check_match_parameters_tcp(match_parameters)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        dl_type = ether_types.ETH_TYPE_IP
        nw_protocol = in_proto.IPPROTO_TCP

        match = parser.OFPMatch(
                                 in_port = input_port,
                                 eth_type = dl_type,
                                 ip_proto = nw_protocol,
                                 ** match_parameters
                               )
        return match

    def build_actions(self, switch_identifier, action_parameters):
        # PRE-CONDITIONS
        self.check_switch_identifier(switch_identifier)
        # action_parameters: check delegated to the __build_action() method
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        actions = []
        for action_parameter in action_parameters:
            action = self.__build_action(switch_identifier, action_parameter)
            if action is not None:
                actions.append(action)

        return actions

    def __build_action(self, switch_identifier, action_parameter):
        # PRE-CONDITIONS
        # switch_identifier: check delegated to the calling method
        self.check_action_parameter(action_parameter)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        action_tuple = action_parameter
        if isinstance(action_tuple, basestring):
            action_tuple = (action_tuple, -1)

        action_type = action_tuple[0]
        action_value = action_tuple[1]

        if action_type == "DROP":
            action = None
            return action
        elif action_type == "OUTPUT":
            action = parser.OFPActionOutput(port = action_value)
            return action
        elif action_type == "SET-QUEUE":
            action = parser.OFPActionSetQueue(queue_id = action_value)
            return action
        elif action_type == "GROUP":
            action = parser.OFPActionGroup(group_id = action_value)
            return action

        # should not reach this line

    def build_group(self, switch_identifier, group_type, group_identifier, buckets):
        # PRE-CONDITIONS
        self.check_switch_identifier(switch_identifier)
        self.check_group_type(group_type)
        self.check_group_identifier(group_identifier)
        self.check_buckets(buckets)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        group_type_identifier = self.from_group_type_to_group_type_identifier[group_type]

        group = parser.OFPGroupMod(switch_datapath, ofproto.OFPGC_ADD, group_type_identifier, group_identifier, buckets)
        switch_datapath.send_msg(group)

    def build_bucket(self, switch_identifier, actions, weight = 1):
        # PRE-CONDITIONS
        self.check_switch_identifier(switch_identifier)
        self.check_actions(actions)
        self.check_weight(weight)
        # ---

        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        watch_port = ofproto_v1_3.OFPP_ANY
        watch_group = ofproto_v1_3.OFPQ_ALL

        bucket = parser.OFPBucket(weight, watch_port, watch_group, actions)
        return bucket

    # ---

    # Flow pre-conditions

    def check_switch_identifier(self, switch_identifier):
        if not self.exists_switch(switch_identifier):
            error_message = "unknown switch_identifier"
            raise NameError(error_message)

    def check_priority(self, priority):
        if priority not in self.from_packet_type_to_flow_rule_priority.values():
            error_message = "unknown priority"
            raise NameError(error_message)

    def check_match(self, match):
        if not isinstance(match, OFPMatch):
            error_message = "match has to be an instance of OFPMatch"
            raise NameError(error_message)

    def check_actions(self, actions):
        if not isinstance(actions, list):
            error_message = "actions has to be a list."
            raise NameError(error_message)

        if not all( isinstance(action, OFPAction) for action in actions):
            error_message = "actions has to be a list of OFPAction."
            raise NameError(error_message)

    def check_idle_timeout(self, idle_timeout):
        if not isinstance(idle_timeout, int):
            error_message = "idle_timeout has to be an integer"
            raise NameError(error_message)

        if idle_timeout < 0:
            error_message = "idle_timeout has to be greater or equal to 0"
            raise NameError(error_message)

    def check_hard_timeout(self, hard_timeout):
        if not isinstance(hard_timeout, int):
            error_message = "hard_timeout has to be an integer"
            raise NameError(error_message)

        if hard_timeout < 0:
            error_message = "hard_timeout has to be greater or equal to 0"
            raise NameError(error_message)

    def check_packet_type(self, packet_type):
        if packet_type not in self.from_packet_type_to_flow_rule_priority.keys():
            error_message = "packet_type can be only [ARP, ICMP, UDP, TCP]".format(packet_type)
            raise NameError(error_message)

    def check_input_port(self, input_port):
        if not isinstance(input_port, int):
            error_message = "input_port has to be an integer"
            raise NameError(error_message)

        if input_port < 0:
            error_message = "input_port has to be greater or equal to 0"
            raise NameError(error_message)

    def check_match_parameters_arp(self, match_parameters):
        if "dl_src" in match_parameters.keys():
            parameter_value = match_parameters["dl_src"]
            del match_parameters["dl_src"]
            match_parameters["eth_src"] = parameter_value

        if "dl_dst" in match_parameters.keys():
            parameter_value = match_parameters["dl_dst"]
            del match_parameters["dl_dst"]
            match_parameters["eth_dst"] = parameter_value

    def check_match_parameters_icmp(self, match_parameters):
        if "nw_src" in match_parameters.keys():
            parameter_value = match_parameters["nw_src"]
            del match_parameters["nw_src"]
            match_parameters["ipv4_src"] = parameter_value

        if "nw_dst" in match_parameters.keys():
            parameter_value = match_parameters["nw_dst"]
            del match_parameters["nw_dst"]
            match_parameters["ipv4_dst"] = parameter_value

    def check_match_parameters_udp(self, match_parameters):
        if "nw_src" in match_parameters.keys():
            parameter_value = match_parameters["nw_src"]
            del match_parameters["nw_src"]
            match_parameters["ipv4_src"] = parameter_value

        if "nw_dst" in match_parameters.keys():
            parameter_value = match_parameters["nw_dst"]
            del match_parameters["nw_dst"]
            match_parameters["ipv4_dst"] = parameter_value

        if "tp_src" in match_parameters.keys():
            parameter_value = match_parameters["tp_src"]
            del match_parameters["tp_src"]
            match_parameters["udp_src"] = parameter_value

        if "tp_dst" in match_parameters.keys():
            parameter_value = match_parameters["tp_dst"]
            del match_parameters["tp_dst"]
            match_parameters["udp_dst"] = parameter_value

    def check_match_parameters_tcp(self, match_parameters):
        if "nw_src" in match_parameters.keys():
            parameter_value = match_parameters["nw_src"]
            del match_parameters["nw_src"]
            match_parameters["ipv4_src"] = parameter_value

        if "nw_dst" in match_parameters.keys():
            parameter_value = match_parameters["nw_dst"]
            del match_parameters["nw_dst"]
            match_parameters["ipv4_dst"] = parameter_value

        if "tp_src" in match_parameters.keys():
            parameter_value = match_parameters["tp_src"]
            del match_parameters["tp_src"]
            match_parameters["tcp_src"] = parameter_value

        if "tp_dst" in match_parameters.keys():
            parameter_value = match_parameters["tp_dst"]
            del match_parameters["tp_dst"]
            match_parameters["tcp_dst"] = parameter_value

    def check_action_parameter(self, action_parameter):
        if isinstance(action_parameter, basestring):
            if not action_parameter == "DROP":
                error_message = "invalid action_parameter"
                raise NameError(error_message)
        else:
            if not isinstance(action_parameter, tuple):
                error_message = "invalid action_parameter"
                raise NameError(error_message)

            if not action_parameter.__len__() == 2:
                error_message = "invalid action_parameter"
                raise NameError(error_message)

            action_name = action_parameter[0]
            action_value = action_parameter[1]

            if not action_name == "SET-QUEUE" and not action_name == "OUTPUT" and not action_name == "GROUP":
                error_message = "invalid action_parameter"
                raise NameError(error_message)

            if not isinstance(action_value, int):
                error_message = "invalid action_parameter"
                raise NameError(error_message)

            if action_value < 0:
                error_message = "invalid action_parameter"
                raise NameError(error_message)

    def check_group_type(self, group_type):
        if group_type not in self.from_group_type_to_group_type_identifier.keys():
            error_message = "group_type can be only [ALL, SELECT, INDIRECT, FAST-FAILURE]"
            raise NameError(error_message)

    def check_group_identifier(self, group_identifier):
        if not isinstance(group_identifier, int):
            error_message = "group_identifier has to be an integer"
            raise NameError(error_message)

        if group_identifier < 0:
            error_message = "group_identifier has to be greater or equal to 0"
            raise NameError(error_message)

    def check_buckets(self, buckets):
        if not isinstance(buckets, list):
            error_message = "buckets has to be a list."
            raise NameError(error_message)

        if not all( isinstance(bucket, OFPBucket) for bucket in buckets):
            error_message = "buckets has to be a list of OFPBucket."
            raise NameError(error_message)

    def check_weight(self, weight):
        if not isinstance(weight, int):
            error_message = "weight has to be an integer"
            raise NameError(error_message)

        if weight < 0 or weight > 10:
            error_message = "weight has to belong to the interval [0, 10]"
            raise NameError(error_message)

    # ---

    # Utility methods

    def get_host_identifier_by_mac_address(self, mac_address_to_find):
        for node in self.topology.nodes(data = "description"):
            identifier = node[0]
            description = node[1]
            node_type = description["type"]
            if node_type == "host":
                mac_address = description["mac_address"]
                if mac_address == mac_address_to_find:
                    return identifier

        return None

    def get_host_identifier_by_ip_address(self, ip_address_to_find):
        for node in self.topology.nodes(data = "description"):
            identifier = node[0]
            description = node[1]
            node_type = description["type"]
            if node_type == "host":
                ip_address = description["ip_address"]
                if ip_address == ip_address_to_find:
                    return identifier

        return None

    # ---


from ryu.lib.packet import ether_types
from ryu.lib.packet import in_proto
from ryu.ofproto import ofproto_v1_3

class FlowManager:

    def __init__(self):
        self.from_switch_identifier_to_switch_datapath = { }

        self.from_group_type_to_group_type_identifier = {
            "ALL": ofproto_v1_3.OFPGT_ALL,
            "SELECT": ofproto_v1_3.OFPGT_SELECT,
            "INDIRECT": ofproto_v1_3.OFPGT_INDIRECT,
            "FAST-FAILURE": ofproto_v1_3.OFPGT_FF
        }

        self.configuration = []

    def send_flow_rules(self, flow_rules):
        for flow_rule in flow_rules:
            self.send_flow_rule(
                flow_rule = flow_rule
            )

    def send_flow_rule(self, flow_rule):
        switch_datapath = flow_rule.datapath
        switch_datapath.send_msg(flow_rule)

    def build_flow_rule(self, switch_identifier, priority, match, actions, idle_timeout = 0, hard_timeout = 0):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        flow_rule = parser.OFPFlowMod(
            datapath = switch_datapath,
            priority = priority,
            match = match,
            instructions = instructions,
            idle_timeout = idle_timeout,
            hard_timeout = hard_timeout
        )
        
        return flow_rule

    def build_match(self, switch_identifier, packet_type, input_port, match_parameters):
        packet_type = packet_type.upper()

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
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

        dl_type = ether_types.ETH_TYPE_ARP

        match = parser.OFPMatch(
            in_port = input_port,
            eth_type = dl_type,
            ** match_parameters
        )

        return match

    def __build_match_icmp(self, switch_identifier, input_port, match_parameters):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

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
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

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
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

        dl_type = ether_types.ETH_TYPE_IP
        nw_protocol = in_proto.IPPROTO_TCP

        match = parser.OFPMatch(
            in_port = input_port,
            eth_type = dl_type,
            ip_proto = nw_protocol,
            ** match_parameters
        )

        return match

    # Available actions: DROP, OUTPUT, SET-QUEUE, GROUP
    def build_actions(self, switch_identifier, actions_parameters):
        actions = []

        for action_parameters in actions_parameters:
            action = self.__build_action(switch_identifier, action_parameters)
            if action is not None:
                actions.append(action)

        return actions

    def __build_action(self, switch_identifier, action_parameters):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser

        action_tuple = action_parameters
        if isinstance(action_tuple, str): # Drop action
            action_tuple = (action_tuple, -1)

        action_type = action_tuple[0]
        action_value = action_tuple[1]

        if action_type == "DROP":
            action = None
            return action
        elif action_type == "OUTPUT":
            action = parser.OFPActionOutput(port=action_value)
            return action
        elif action_type == "SET-QUEUE":
            action = parser.OFPActionSetQueue(queue_id=action_value)
            return action
        elif action_type == "GROUP":
            action = parser.OFPActionGroup(group_id=action_value)
            return action

        # should not reach this line

    def send_groups(self, switch_identifier, groups):
        for group in groups:
            self.send_group(
                switch_identifier = switch_identifier,
                group = group
            )

    def send_group(self, switch_identifier, group):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        switch_datapath.send_msg(group)

    # Available group types: ALL, SELECT, INDIRECT, FAST-FAILURE
    def build_add_group(self, switch_identifier, group_type, group_identifier, buckets):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        group_type_identifier = self.from_group_type_to_group_type_identifier[group_type]

        group = parser.OFPGroupMod(
            switch_datapath,
            ofproto.OFPGC_ADD,
            group_type_identifier,
            group_identifier,
            buckets
        )

        return group

    # Available group types: ALL, SELECT, INDIRECT, FAST-FAILURE
    def build_modify_group(self, switch_identifier, group_type, group_identifier, buckets):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        group_type_identifier = self.from_group_type_to_group_type_identifier[group_type]

        group = parser.OFPGroupMod(
            switch_datapath,
            ofproto.OFPGC_MODIFY,
            group_type_identifier,
            group_identifier,
            buckets
        )

        return group

    def build_bucket(self, switch_identifier, actions, weight = 1):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser

        watch_port = ofproto_v1_3.OFPP_ANY
        watch_group = ofproto_v1_3.OFPQ_ALL

        bucket = parser.OFPBucket(weight, watch_port, watch_group, actions)
        return bucket

    def push_configuration(self, configuration):
        self.configuration = configuration

    def get_configuration(self):
        return self.configuration

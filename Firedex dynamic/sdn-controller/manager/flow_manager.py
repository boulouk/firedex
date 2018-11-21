
from ryu.lib.packet import ether_types
from ryu.lib.packet import in_proto
from ryu.ofproto import ofproto_v1_3

class FlowManager:

    def __init__(self):
        self.from_switch_identifier_to_switch_datapath = { }

    def send_flow_rules(self, flow_rules):
        for flow_rule in flow_rules:
            self.send_flow_rule(
                flow_rule = flow_rule
            )

    def send_flow_rule(self, flow_rule):
        switch_datapath = flow_rule.datapath
        switch_datapath.send_msg(msg = flow_rule)

    def build_add_flow_rule(self, switch_identifier, priority, match, actions, idle_timeout = 0, hard_timeout = 0):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        flow_rule_type = ofproto.OFPFC_ADD
        instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        flow_rule = parser.OFPFlowMod(
            datapath = switch_datapath,
            command = flow_rule_type,
            priority = priority,
            match = match,
            instructions = instructions,
            idle_timeout = idle_timeout,
            hard_timeout = hard_timeout
        )
        
        return flow_rule

    def build_remove_flow_rule(self, switch_identifier, priority, match, actions, idle_timeout = 0, hard_timeout = 0):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        flow_rule_type = ofproto.OFPFC_DELETE
        instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        flow_rule = parser.OFPFlowMod(
            datapath = switch_datapath,
            command = flow_rule_type,
            priority = priority,
            match = match,
            instructions = instructions,
            idle_timeout = idle_timeout,
            hard_timeout = hard_timeout
        )

        return flow_rule

    def build_match(self, switch_identifier, packet_type, match_parameters):
        packet_type = packet_type.upper()

        if packet_type == "ARP":
            match = self.__build_match_arp(
                switch_identifier = switch_identifier,
                match_parameters = match_parameters
            )
            return match
        elif packet_type == "ICMP":
            match = self.__build_match_icmp(
                switch_identifier = switch_identifier,
                match_parameters = match_parameters
            )
            return match
        elif packet_type == "UDP":
            match = self.__build_match_udp(
                switch_identifier = switch_identifier,
                match_parameters = match_parameters
            )
            return match
        elif packet_type == "TCP":
            match = self.__build_match_tcp(
                switch_identifier = switch_identifier,
                match_parameters = match_parameters
            )
            return match

        # should not reach this line

    def __build_match_arp(self, switch_identifier, match_parameters):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

        dl_type = ether_types.ETH_TYPE_ARP

        match = parser.OFPMatch(
            eth_type = dl_type,
            ** match_parameters
        )

        return match

    def __build_match_icmp(self, switch_identifier, match_parameters):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

        dl_type = ether_types.ETH_TYPE_IP
        nw_protocol = in_proto.IPPROTO_ICMP

        match = parser.OFPMatch(
            eth_type = dl_type,
            ip_proto = nw_protocol,
            ** match_parameters
        )

        return match

    def __build_match_udp(self, switch_identifier, match_parameters):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

        dl_type = ether_types.ETH_TYPE_IP
        nw_protocol = in_proto.IPPROTO_UDP

        match = parser.OFPMatch(
            eth_type = dl_type,
            ip_proto = nw_protocol,
            ** match_parameters
        )

        return match

    def __build_match_tcp(self, switch_identifier, match_parameters):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        parser = switch_datapath.ofproto_parser

        dl_type = ether_types.ETH_TYPE_IP
        nw_protocol = in_proto.IPPROTO_TCP

        match = parser.OFPMatch(
            eth_type = dl_type,
            ip_proto = nw_protocol,
            ** match_parameters
        )

        return match

    # Available actions: DROP, OUTPUT, SET-QUEUE, GROUP
    def build_actions(self, switch_identifier, actions_parameters):
        actions = []

        for action_parameters in actions_parameters:
            action = self.__build_action(
                switch_identifier = switch_identifier,
                action_parameters = action_parameters
            )

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
            action = parser.OFPActionOutput(port = action_value)
            return action
        elif action_type == "SET-QUEUE":
            action = parser.OFPActionSetQueue(queue_id = action_value)
            return action
        elif action_type == "GROUP":
            action = parser.OFPActionGroup(group_id = action_value)
            return action

        # should not reach this line

    def send_group_rules(self, switch_identifier, group_rules):
        for group_rule in group_rules:
            self.send_group_rule(
                switch_identifier = switch_identifier,
                group_rule = group_rule
            )

    def send_group_rule(self, switch_identifier, group_rule):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]
        switch_datapath.send_msg(msg = group_rule)

    def build_add_group_rule(self, switch_identifier, group_identifier, buckets):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        group_type = ofproto.OFPGC_ADD

        group_rule = parser.OFPGroupMod(
            datapath = switch_datapath,
            command = group_type,
            type_ = ofproto.OFPGT_SELECT,
            group_id = group_identifier,
            buckets = buckets
        )

        return group_rule

    def build_modify_group_rule(self, switch_identifier, group_identifier, buckets):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        group_type = ofproto.OFPFC_MODIFY

        group_rule = parser.OFPGroupMod(
            datapath = switch_datapath,
            command = group_type,
            type_ = ofproto.OFPGT_SELECT,
            group_id = group_identifier,
            buckets = buckets
        )

        return group_rule

    def build_remove_group_rule(self, switch_identifier, group_identifier, buckets):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser
        ofproto = switch_datapath.ofproto

        group_type = ofproto.OFPGC_DELETE

        group_rule = parser.OFPGroupMod(
            datapath = switch_datapath,
            command = group_type,
            type_ = ofproto.OFPGT_SELECT,
            group_id = group_identifier,
            buckets = buckets
        )

        return group_rule

    def build_bucket(self, switch_identifier, actions, weight = 1):
        switch_datapath = self.from_switch_identifier_to_switch_datapath[switch_identifier]

        parser = switch_datapath.ofproto_parser

        watch_port = ofproto_v1_3.OFPP_ANY
        watch_group = ofproto_v1_3.OFPQ_ALL

        bucket = parser.OFPBucket(
            weight = weight,
            watch_port = watch_port,
            watch_group = watch_group,
            actions = actions
        )

        return bucket

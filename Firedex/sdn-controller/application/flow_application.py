
import json, requests

from manager.flow_manager import FlowManager

from ryu.app import wsgi
from ryu.app.wsgi import Response, ControllerBase
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import icmp
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.topology import event

from utility.naming_utility import *

class FlowController(ControllerBase):

    def __init__(self, request, link, data, **configuration):
        super(FlowController, self).__init__(request, link, data, **configuration)

    def send_flow_rule(self, request, **kwargs):
        flow_manager = self.parent.registory["FlowManager"]

        flow_rule_parameters = request.json

        switch_identifier = flow_rule_parameters["switch_identifier"]
        priority = flow_rule_parameters["priority"]
        packet_type = flow_rule_parameters["packet_type"]
        input_port = flow_rule_parameters["input_port"]
        match_parameters = flow_rule_parameters["match_parameters"]
        actions_parameters = flow_rule_parameters["actions_parameters"]

        match = flow_manager.build_match(
            switch_identifier = switch_identifier,
            packet_type = packet_type,
            input_port = input_port,
            match_parameters = match_parameters
        )

        new_actions_parameters = []
        for action_parameters in actions_parameters:
            if action_parameters.__len__() == 1:
                new_actions_parameters.append( action_parameters[0] )
            elif action_parameters.__len__() == 2:
                new_actions_parameters.append( (action_parameters[0], action_parameters[1]) )

        actions = flow_manager.build_actions(
            switch_identifier = switch_identifier,
            actions_parameters = new_actions_parameters
        )

        flow_rule = flow_manager.build_flow_rule(
            switch_identifier = switch_identifier,
            priority = priority,
            match = match,
            actions = actions
        )

        flow_manager.send_flow_rule(flow_rule)

        result = {
            "flow_rule": flow_rule_parameters,
            "result": "successful"
        }

        body = json.dumps(result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def send_add_group(self, request, **kwargs):
        flow_manager = self.parent.registory["FlowManager"]

        group_parameters = request.json

        switch_identifier = group_parameters["switch_identifier"]
        group_type = group_parameters["group_type"]
        group_identifier = group_parameters["group_identifier"]
        buckets_parameters = group_parameters["buckets"]

        buckets = []

        for bucket_parameters in buckets_parameters:
            actions_parameters = bucket_parameters["actions"]

            new_actions_parameters = []
            for action_parameters in actions_parameters:
                if action_parameters.__len__() == 1:
                    new_actions_parameters.append( action_parameters[0] )
                elif action_parameters.__len__() == 2:
                    new_actions_parameters.append( (action_parameters[0], action_parameters[1]) )

            actions = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = new_actions_parameters
            )

            weight = bucket_parameters["weight"]

            bucket = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions,
                weight = weight
            )

            buckets.append(bucket)

        group = flow_manager.build_add_group(
            switch_identifier = switch_identifier,
            group_type = group_type,
            group_identifier = group_identifier,
            buckets = buckets
        )

        flow_manager.send_group(switch_identifier, group)

        result = {
            "flow_rule": group_parameters,
            "result": "successful"
        }

        body = json.dumps(result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def send_modify_group(self, request, **kwargs):
        flow_manager = self.parent.registory["FlowManager"]

        group_parameters = request.json

        switch_identifier = group_parameters["switch_identifier"]
        group_type = group_parameters["group_type"]
        group_identifier = group_parameters["group_identifier"]
        buckets_parameters = group_parameters["buckets"]

        buckets = []

        for bucket_parameters in buckets_parameters:
            actions_parameters = bucket_parameters["actions"]

            new_actions_parameters = []
            for action_parameters in actions_parameters:
                if action_parameters.__len__() == 1:
                    new_actions_parameters.append(action_parameters[0])
                elif action_parameters.__len__() == 2:
                    new_actions_parameters.append((action_parameters[0], action_parameters[1]))

            actions = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = new_actions_parameters
            )

            weight = bucket_parameters["weight"]

            bucket = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions,
                weight = weight
            )

            buckets.append(bucket)

        group = flow_manager.build_modify_group(
            switch_identifier = switch_identifier,
            group_type = group_type,
            group_identifier = group_identifier,
            buckets = buckets
        )

        flow_manager.send_group(switch_identifier, group)

        result = {
            "flow_rule": group_parameters,
            "result": "successful"
        }

        body = json.dumps(result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def push_configuration(self, request, **kwargs):
        flow_manager = self.parent.registory["FlowManager"]

        configuration = request.json
        flow_manager.push_configuration(configuration)

        result = {
            "result": "successful"
        }

        body = json.dumps(result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        print(configuration)

        return response

class FlowApplication(app_manager.RyuApp):
    _DEFAULT_PRIORITY = 1
    _CONTEXTS = {"wsgi": wsgi.WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(FlowApplication, self).__init__(*args, **kwargs)
        self.flow_manager = FlowManager()

        wsgi = kwargs['wsgi']
        wsgi.registory["FlowManager"] = self.flow_manager

        mapper = wsgi.mapper

        mapper.connect(
            "Add flow",
            "/api/flow/send-flow-rule/",
            controller = FlowController,
            action = "send_flow_rule",
            conditions = {"method": "POST"}
        )

        mapper.connect(
            "Add group",
            "/api/flow/send-group/",
            controller = FlowController,
            action = "send_add_group",
            conditions = {"method": "POST"}
        )

        mapper.connect(
            "Modify group",
            "/api/flow/modify-group/",
            controller = FlowController,
            action = "send_modify_group",
            conditions = {"method": "POST"}
        )

        mapper.connect(
            "Push configuration",
            "/api/flow/push-configuration/",
            controller = FlowController,
            action = "push_configuration",
            conditions = {"method": "POST"}
        )

    @set_ev_cls(event.EventSwitchEnter)
    def event_switch_enter(self, event_switch_enter):
        switch_datapath = event_switch_enter.switch.dp
        switch_identifier = switch_datapath.id
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_identifier)

        self.flow_manager.from_switch_identifier_to_switch_datapath[switch_identifier] = switch_datapath

    @set_ev_cls(event.EventSwitchLeave)
    def event_switch_leave(self, event_switch_leave):
        switch_datapath = event_switch_leave.switch.dp
        switch_identifier = switch_datapath.id
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_identifier)

        del self.flow_manager.from_switch_identifier_to_switch_datapath[switch_identifier]

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def on_packet_in(self, event):
        message = event.msg
        switch_datapath = message.datapath
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_datapath.id)
        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        input_packet = packet.Packet(message.data)

        input_port = message.match["in_port"]

        ethernet_packet = input_packet.get_protocol(ethernet.ethernet)

        dl_src = ethernet_packet.src
        dl_dst = ethernet_packet.dst
        dl_type = ethernet_packet.ethertype

        if dl_type == ether_types.ETH_TYPE_LLDP:
            return

        arp_packet = input_packet.get_protocol(arp.arp)
        ipv4_packet = input_packet.get_protocol(ipv4.ipv4)
        ipv6_packet = input_packet.get_protocol(ipv6.ipv6)
        icmp_packet = input_packet.get_protocol(icmp.icmp)
        udp_packet = input_packet.get_protocol(udp.udp)
        tcp_packet = input_packet.get_protocol(tcp.tcp)

        if arp_packet:
            dl_src = arp_packet.src_mac
            dl_dst = arp_packet.dst_mac
            nw_src = arp_packet.src_ip
            nw_dst = arp_packet.dst_ip

            output_port = self.__output_port(switch_identifier, dl_dst)

            if output_port != "None":
                match_parameters = {
                    "eth_src": dl_src,
                    "eth_dst": dl_dst
                }

                actions_parameters = [
                    ("OUTPUT", output_port)
                ]

                self.__send_flow_rule(
                    switch_identifier = switch_identifier,
                    input_port = input_port,
                    output_port = output_port,
                    packet_type = "ARP",
                    match_parameters = match_parameters,
                    actions_parameters = actions_parameters
                )

            self.__handle_packet(
                message = message,
                switch_identifier = switch_identifier,
                switch_datapath = switch_datapath,
                input_port = input_port,
                output_port = output_port
            )

        elif ipv4_packet:
            if icmp_packet:
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst

                output_port = self.__output_port(switch_identifier, dl_dst)

                if output_port != "None":
                    match_parameters = {
                        "eth_src": dl_src,
                        "eth_dst": dl_dst,
                        "ipv4_src": nw_src,
                        "ipv4_dst": nw_dst
                    }

                    actions_parameters = [
                        ("OUTPUT", output_port)
                    ]

                    self.__send_flow_rule(
                        switch_identifier = switch_identifier,
                        input_port = input_port,
                        output_port = output_port,
                        packet_type = "ICMP",
                        match_parameters = match_parameters,
                        actions_parameters = actions_parameters
                    )

                self.__handle_packet(
                    message = message,
                    switch_identifier = switch_identifier,
                    switch_datapath = switch_datapath,
                    input_port = input_port,
                    output_port = output_port
                )

            elif udp_packet:
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst
                tp_src = udp_packet.src_port
                tp_dst = udp_packet.dst_port

                output_port = self.__output_port(switch_identifier, dl_dst)

                if output_port != "None":
                    match_parameters = {
                        "eth_src": dl_src,
                        "eth_dst": dl_dst,
                        "ipv4_src": nw_src,
                        "ipv4_dst": nw_dst,
                        "udp_src": tp_src,
                        "udp_dst": tp_dst
                    }

                    actions_parameters = []

                    prioritize = False
                    system_state = self.flow_manager.configuration

                    # target_switch = "S6149008586379938817"
                    target_switch = "S254"

                    # DROP RATES AND PRIORITIES
                    if switch_identifier == target_switch:
                        for system_state_entry in system_state:
                            host = system_state_entry["network_flow"]["host"]
                            port = system_state_entry["network_flow"]["port"]

                            if host == nw_dst and port == tp_dst:

                                a = int( host.split(".")[-1] )
                                b = int( port )
                                print(a, b)

                                group_identifier = int(  ( (a + b) * (a + b + 1) ) / 2 + b  )
                                print(group_identifier)

                                priority = system_state_entry["priority"]
                                drop_rate = int( float(system_state_entry["drop_rate"]) * 100 )

                                actions_output = self.flow_manager.build_actions(switch_identifier, [ ("SET-QUEUE", priority), ("OUTPUT", output_port) ])
                                actions_drop = self.flow_manager.build_actions(switch_identifier, [ "DROP" ])

                                bucket_output = self.flow_manager.build_bucket(switch_identifier, actions_output, 100 - drop_rate)
                                bucket_drop = self.flow_manager.build_bucket(switch_identifier, actions_drop, drop_rate)
                                buckets = [ bucket_output, bucket_drop ]

                                group = self.flow_manager.build_add_group(switch_identifier, "SELECT", group_identifier, buckets)
                                self.flow_manager.send_group(switch_identifier, group)

                                actions_parameters = [
                                    ("GROUP", group_identifier)
                                ]

                                prioritize = True

                    if switch_identifier != target_switch or not prioritize:
                        actions_parameters = [
                            ("OUTPUT", output_port)
                        ]

                    # PRIORITIES, NO DROP RATES
                    # if switch_identifier == target_switch:
                    #     for system_state_entry in system_state:
                    #         host = system_state_entry["network_flow"]["host"]
                    #         port = system_state_entry["network_flow"]["port"]
                    #
                    #         if host == nw_dst and port == tp_dst:
                    #             priority = system_state_entry["priority"]
                    #
                    #             actions_parameters = [
                    #                 ("SET-QUEUE", priority),
                    #                 ("OUTPUT", output_port)
                    #             ]
                    #
                    #             prioritize = True
                    #
                    # if switch_identifier != target_switch or not prioritize:
                    #     actions_parameters = [
                    #         ("OUTPUT", output_port)
                    #     ]

                    # NO DROP RATES, NO PRIORITIES
                    # actions_parameters = [
                    #     ("OUTPUT", output_port)
                    # ]

                    self.__send_flow_rule(
                        switch_identifier = switch_identifier,
                        input_port = input_port,
                        output_port = output_port,
                        packet_type = "UDP",
                        match_parameters = match_parameters,
                        actions_parameters = actions_parameters
                    )

                self.__handle_packet(
                    message = message,
                    switch_identifier = switch_identifier,
                    switch_datapath = switch_datapath,
                    input_port = input_port,
                    output_port = output_port
                )

            elif tcp_packet:
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst
                tp_src = tcp_packet.src_port
                tp_dst = tcp_packet.dst_port

                output_port = self.__output_port(switch_identifier, dl_dst)

                if output_port != "None":
                    match_parameters = {
                        "eth_src": dl_src,
                        "eth_dst": dl_dst,
                        "ipv4_src": nw_src,
                        "ipv4_dst": nw_dst,
                        "tcp_src": tp_src,
                        "tcp_dst": tp_dst
                    }

                    actions_parameters = [
                        ("OUTPUT", output_port)
                    ]

                    self.__send_flow_rule(
                        switch_identifier = switch_identifier,
                        input_port = input_port,
                        output_port = output_port,
                        packet_type = "TCP",
                        match_parameters = match_parameters,
                        actions_parameters = actions_parameters
                    )

                self.__handle_packet(
                    message = message,
                    switch_identifier = switch_identifier,
                    switch_datapath = switch_datapath,
                    input_port = input_port,
                    output_port = output_port
                )

        elif ipv6_packet:
            pass

        else:
            self.__flood_packet(
                message = message,
                switch_datapath = switch_datapath,
                input_port = input_port
            )

    def __output_port(self, source_identifier, destination_identifier):
        url = "http://127.0.0.1:8080/api/topology/output-port/"
        data = " { \"source_identifier\": \"%s\", \"destination_identifier\": \"%s\" }" % (source_identifier, destination_identifier)
        response = requests.post(url, data = data)
        content = response.json()
        output_port = content["output_port"]
        return output_port

    def __drop_rate(self, priority):
        url = "http://10.0.2.15:5000/api/firedex/drop-rates/"
        response = requests.get(url)
        drop_rates = response.json()

        from_priority_to_drop_rate = { }

        for drop_rate in drop_rates:
            from_priority_to_drop_rate[drop_rate["priority"]] = drop_rate["drop_rate"]

        return drop_rates[priority]["drop_rate"]

    def __send_add_group(self, switch_identifier, group_identifier, drop_rate, priority, output_port):
        drop_actions = self.flow_manager.build_actions(
            switch_identifier = switch_identifier,
            actions_parameters=["DROP"]
        )

        drop_bucket = self.flow_manager.build_bucket(
            switch_identifier = switch_identifier,
            actions = drop_actions,
            weight = drop_rate
        )

        enqueue_actions = self.flow_manager.build_actions(
            switch_identifier = switch_identifier,
            actions_parameters = [ ("SET-QUEUE", priority), ("OUTPUT", output_port) ]
        )

        enqueue_bucket = self.flow_manager.build_bucket(
            switch_identifier = switch_identifier,
            actions = enqueue_actions,
            weight = (10 - drop_rate)
        )

        buckets = [ enqueue_bucket, drop_bucket ]

        group = self.flow_manager.build_add_group(
            switch_identifier = switch_identifier,
            group_type = "SELECT",
            group_identifier = group_identifier,
            buckets = buckets
        )

        self.flow_manager.send_group(
            switch_identifier = switch_identifier,
            group = group
        )

    def __send_flow_rule(self, switch_identifier, input_port, output_port, packet_type, match_parameters, actions_parameters):
        match = self.flow_manager.build_match(
            switch_identifier = switch_identifier,
            packet_type = packet_type,
            input_port = input_port,
            match_parameters = match_parameters
        )

        actions = self.flow_manager.build_actions(
            switch_identifier = switch_identifier,
            actions_parameters = actions_parameters
        )

        flow_rule = self.flow_manager.build_flow_rule(
            switch_identifier = switch_identifier,
            priority = self._DEFAULT_PRIORITY,
            match = match,
            actions = actions
        )

        self.flow_manager.send_flow_rule(
            flow_rule = flow_rule
        )

    def __handle_packet(self, message, switch_identifier, switch_datapath, input_port, output_port):
        if output_port == "None":
            self.__flood_packet(
                message = message,
                switch_datapath = switch_datapath,
                input_port = input_port
            )
        else:
            self.__send_packet(
                message = message,
                switch_datapath = switch_datapath,
                input_port = input_port,
                output_port = output_port
            )

    def __flood_packet(self, message, switch_datapath, input_port):
        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        output_port = ofproto.OFPP_FLOOD
        self.__send_packet(message, switch_datapath, input_port, output_port)

    def __send_packet(self, message, switch_datapath, input_port, output_port):
        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        actions = [ parser.OFPActionOutput(output_port) ]

        buffer_identifier = message.buffer_id
        data = None
        if buffer_identifier == ofproto.OFP_NO_BUFFER:
            data = message.data

        output_packet = parser.OFPPacketOut(
            datapath = switch_datapath,
            buffer_id = buffer_identifier,
            in_port = input_port,
            actions = actions,
            data = data
        )

        switch_datapath.send_msg(output_packet)

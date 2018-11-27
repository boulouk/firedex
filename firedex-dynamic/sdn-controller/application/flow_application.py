
import json
import requests

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
    _FIREDEX_PRIORITY = 2

    def __init__(self, request, link, data, **configuration):
        super(FlowController, self).__init__(request, link, data, **configuration)

    def add_firedex_policies(self, request, **kwargs):
        flow_manager = self.parent.registory["FlowManager"]

        firedex_policy_parameters = request.json

        switch_identifier = firedex_policy_parameters["switch_identifier"]
        policies = firedex_policy_parameters["policies"]

        for policy in policies:
            destination_ip_address = policy["destination_ip_address"]
            destination_transport_port = policy["destination_transport_port"]
            priority = policy["priority"]
            drop_rate = int( policy["drop_rate"] * 100 )

            output_port = self.__output_port_to_ip_address(switch_identifier, destination_ip_address)

            a = int( destination_ip_address.split(".")[-1] )
            b = int( destination_transport_port )

            group_identifier = int(  ( (a + b) * (a + b + 1) ) / 2 + b  )

            actions_output = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = [ ("SET-QUEUE", priority), ("OUTPUT", output_port) ]
            )

            actions_drop = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = ["DROP"]
            )

            bucket_output = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions_output,
                weight = 100 - drop_rate
            )

            bucket_drop = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions_drop,
                weight = drop_rate
            )

            buckets = [bucket_output, bucket_drop]

            group_rule = flow_manager.build_add_group_rule(
                switch_identifier = switch_identifier,
                group_identifier = group_identifier,
                buckets = buckets
            )

            flow_manager.send_group_rule(
                switch_identifier = switch_identifier,
                group_rule = group_rule
            )

            match_parameters = {
                "ipv4_dst": destination_ip_address,
                "udp_dst": destination_transport_port
            }

            actions_parameters = [
                ("GROUP", group_identifier)
            ]

            match = flow_manager.build_match(
                switch_identifier = switch_identifier,
                packet_type = "UDP",
                match_parameters = match_parameters
            )

            actions = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = actions_parameters
            )

            flow_rule = flow_manager.build_add_flow_rule(
                switch_identifier = switch_identifier,
                priority = self._FIREDEX_PRIORITY,
                match = match,
                actions = actions
            )

            flow_manager.send_flow_rule(
                flow_rule = flow_rule
            )

        result = {
            "result": "successful"
        }

        body = json.dumps(obj = result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def modify_firedex_policies(self, request, **kwargs):
        flow_manager = self.parent.registory["FlowManager"]

        firedex_policy_parameters = request.json

        switch_identifier = firedex_policy_parameters["switch_identifier"]
        policies = firedex_policy_parameters["policies"]

        for policy in policies:
            destination_ip_address = policy["destination_ip_address"]
            destination_transport_port = policy["destination_transport_port"]
            priority = policy["priority"]
            drop_rate = int( policy["drop_rate"] * 100 )

            output_port = self.__output_port_to_ip_address(switch_identifier, destination_ip_address)

            a = int( destination_ip_address.split(".")[-1] )
            b = int( destination_transport_port )

            group_identifier = int(  ( (a + b) * (a + b + 1) ) / 2 + b  )

            actions_output = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = [("SET-QUEUE", priority), ("OUTPUT", output_port)]
            )

            actions_drop = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = ["DROP"]
            )

            bucket_output = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions_output,
                weight = 100 - drop_rate
            )

            bucket_drop = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions_drop,
                weight = drop_rate
            )

            buckets = [bucket_output, bucket_drop]

            group_rule = flow_manager.build_modify_group_rule(
                switch_identifier = switch_identifier,
                group_identifier = group_identifier,
                buckets = buckets
            )

            flow_manager.send_group_rule(
                switch_identifier = switch_identifier,
                group_rule = group_rule
            )

        result = {
            "result": "successful"
        }

        body = json.dumps(obj = result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def remove_firedex_policies(self, request, **kwargs):
        flow_manager = self.parent.registory["FlowManager"]

        firedex_policy_parameters = request.json

        switch_identifier = firedex_policy_parameters["switch_identifier"]
        policies = firedex_policy_parameters["policies"]

        for policy in policies:
            destination_ip_address = policy["destination_ip_address"]
            destination_transport_port = policy["destination_transport_port"]
            priority = policy["priority"]
            drop_rate = int( policy["drop_rate"] * 100 )

            output_port = self.__output_port_to_ip_address(switch_identifier, destination_ip_address)

            a = int( destination_ip_address.split(".")[-1] )
            b = int( destination_transport_port )

            group_identifier = int(  ( (a + b) * (a + b + 1) ) / 2 + b  )

            actions_output = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = [("SET-QUEUE", priority), ("OUTPUT", output_port)]
            )

            actions_drop = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = ["DROP"]
            )

            bucket_output = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions_output,
                weight = 100 - drop_rate
            )

            bucket_drop = flow_manager.build_bucket(
                switch_identifier = switch_identifier,
                actions = actions_drop,
                weight = drop_rate
            )

            buckets = [bucket_output, bucket_drop]

            group_rule = flow_manager.build_remove_group_rule(
                switch_identifier = switch_identifier,
                group_identifier = group_identifier,
                buckets = buckets
            )

            flow_manager.send_group_rule(
                switch_identifier = switch_identifier,
                group_rule = group_rule
            )

            match_parameters = {
                "ipv4_dst": destination_ip_address,
                "udp_dst": destination_transport_port
            }

            actions_parameters = [
                ("GROUP", group_identifier)
            ]

            match = flow_manager.build_match(
                switch_identifier = switch_identifier,
                packet_type = "UDP",
                match_parameters = match_parameters
            )

            actions = flow_manager.build_actions(
                switch_identifier = switch_identifier,
                actions_parameters = actions_parameters
            )

            flow_rule = flow_manager.build_remove_flow_rule(
                switch_identifier = switch_identifier,
                priority = self._FIREDEX_PRIORITY,
                match = match,
                actions = actions
            )

            flow_manager.send_flow_rule(
                flow_rule = flow_rule
            )

        result = {
            "result": "successful"
        }

        body = json.dumps(obj = result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def __output_port_to_ip_address(self, source_identifier, destination_ip_address):
        url = "http://127.0.0.1:8080/api/topology/output-port-to-ip-address/"

        data = {
            "source_identifier": source_identifier,
            "destination_ip_address": destination_ip_address
        }
        data = json.dumps(obj = data)

        response = requests.post(
            url = url,
            data = data
        )

        content = response.json()
        output_port = content["output_port"]
        return output_port

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
            "Add FireDeX policies",
            "/api/flow/add-firedex-policies/",
            controller = FlowController,
            action = "add_firedex_policies",
            conditions = {"method": "POST"}
        )

        mapper.connect(
            "Modify FireDeX policies",
            "/api/flow/modify-firedex-policies/",
            controller = FlowController,
            action = "modify_firedex_policies",
            conditions = {"method": "POST"}
        )

        mapper.connect(
            "Remove FireDeX policies",
            "/api/flow/remove-firedex-policies/",
            controller = FlowController,
            action = "remove_firedex_policies",
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

            output_port = self.__output_port_to_mac_address(
                source_identifier = switch_identifier,
                destination_mac_address = dl_dst
            )

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
                    output_port = output_port,
                    packet_type = "ARP",
                    match_parameters = match_parameters,
                    actions_parameters = actions_parameters
                )

            self.__handle_packet(
                message = message,
                switch_datapath = switch_datapath,
                input_port = input_port,
                output_port = output_port
            )

        elif ipv4_packet:
            if icmp_packet:
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst

                output_port = self.__output_port_to_mac_address(switch_identifier, dl_dst)

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
                        output_port = output_port,
                        packet_type = "ICMP",
                        match_parameters = match_parameters,
                        actions_parameters = actions_parameters
                    )

                self.__handle_packet(
                    message = message,
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

                output_port = self.__output_port_to_mac_address(switch_identifier, dl_dst)

                if output_port != "None":
                    match_parameters = {
                        "eth_src": dl_src,
                        "eth_dst": dl_dst,
                        "ipv4_src": nw_src,
                        "ipv4_dst": nw_dst,
                        "udp_src": tp_src,
                        "udp_dst": tp_dst
                    }

                    actions_parameters = [
                        ("OUTPUT", output_port)
                    ]

                    self.__send_flow_rule(
                        switch_identifier = switch_identifier,
                        output_port = output_port,
                        packet_type = "UDP",
                        match_parameters = match_parameters,
                        actions_parameters = actions_parameters
                    )

                self.__handle_packet(
                    message = message,
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

                output_port = self.__output_port_to_mac_address(switch_identifier, dl_dst)

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
                        output_port = output_port,
                        packet_type = "TCP",
                        match_parameters = match_parameters,
                        actions_parameters = actions_parameters
                    )

                self.__handle_packet(
                    message = message,
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

    def __output_port_to_mac_address(self, source_identifier, destination_mac_address):
        url = "http://127.0.0.1:8080/api/topology/output-port-to-mac-address/"

        data = {
            "source_identifier": source_identifier,
            "destination_mac_address": destination_mac_address
        }
        data = json.dumps(obj = data)

        response = requests.post(
            url = url,
            data = data
        )

        content = response.json()
        output_port = content["output_port"]
        return output_port

    def __send_flow_rule(self, switch_identifier, output_port, packet_type, match_parameters, actions_parameters):
        match = self.flow_manager.build_match(
            switch_identifier = switch_identifier,
            packet_type = packet_type,
            match_parameters = match_parameters
        )

        actions = self.flow_manager.build_actions(
            switch_identifier = switch_identifier,
            actions_parameters = actions_parameters
        )

        flow_rule = self.flow_manager.build_add_flow_rule(
            switch_identifier = switch_identifier,
            priority = self._DEFAULT_PRIORITY,
            match = match,
            actions = actions
        )

        self.flow_manager.send_flow_rule(
            flow_rule = flow_rule
        )

    def __handle_packet(self, message, switch_datapath, input_port, output_port):
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
        self.__send_packet(
            message = message,
            switch_datapath = switch_datapath,
            input_port = input_port,
            output_port = output_port
        )

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

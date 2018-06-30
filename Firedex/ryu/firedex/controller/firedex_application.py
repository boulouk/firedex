
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import icmp
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls

from firedex_controller import FiredexController
from naming_utility import *

class FiredexApplication(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(FiredexApplication, self).__init__(*args, **kwargs)
        self.firedex_controller = FiredexController()

    def get_firedex_controller(self):
        return self.firedex_controller

    @set_ev_cls(event.EventSwitchEnter)
    def on_switch_enter(self, event):
        self.refresh_topology()

    @set_ev_cls(event.EventSwitchLeave)
    def on_switch_leave(self, event):
        self.refresh_topology()

    def refresh_topology(self):
        self.firedex_controller.clear_topology()

        # get switches
        switches = get_switch(self, None)

        for switch in switches:
            switch_identifier = switch.dp.id
            switch_datapath = switch.dp

            identifier = switch_from_identifier(switch_identifier)

            self.firedex_controller.add_switch(identifier, switch_datapath)

        # get links between switches
        links = get_link(self, None)

        for link in links:
            identifier_1 = switch_from_identifier(link.src.dpid)
            identifier_2 = switch_from_identifier(link.dst.dpid)
            port_1 = link.src.port_no
            port_2 = link.dst.port_no

            self.firedex_controller.add_link(identifier_1, identifier_2, port_1, port_2)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def on_packet_in(self, event):
        message = event.msg # packet-in message
        datapath = message.datapath # switch information
        switch_identifier = switch_from_identifier(datapath.id)
        ofproto = datapath.ofproto # protocol information
        parser = datapath.ofproto_parser # protocol parser

        # input_port = message.in_port # for mininet experiments
        input_port = message.match["in_port"]

        input_packet = packet.Packet(message.data)

        ethernet_packet = input_packet.get_protocol(ethernet.ethernet)
        dl_type = ethernet_packet.ethertype

        if dl_type == ether_types.ETH_TYPE_LLDP:
            return  # ignore lldp packet

        arp_packet = input_packet.get_protocol(arp.arp)
        ipv4_packet = input_packet.get_protocol(ipv4.ipv4)
        icmp_packet = input_packet.get_protocol(icmp.icmp)
        udp_packet = input_packet.get_protocol(udp.udp)
        tcp_packet = input_packet.get_protocol(tcp.tcp)

        if arp_packet:
            dl_src = arp_packet.src_mac # source mac address
            dl_dst = arp_packet.dst_mac # destionation mac address
            nw_src = arp_packet.src_ip # source ip address
            nw_dst = arp_packet.dst_ip # destination ip address

            # learning topology
            host_identifier = identifier_from_mac_address(dl_src)
            host_identifier = host_from_identifier(host_identifier)
            mac_address = dl_src
            ip_address = nw_src

            successful = self.firedex_controller.add_host(host_identifier, mac_address, ip_address)

            if successful:
                identifier_1 = host_identifier
                identifier_2 = switch_identifier
                port_1 = 0
                port_2 = input_port

                self.firedex_controller.add_link(identifier_1, identifier_2, port_1, port_2)
            # ---

            shortest_path = self.firedex_controller.shortest_path(switch_identifier, nw_dst)

            if shortest_path is None:
                self.flood_packet(message, datapath, ofproto, parser, input_port)
            else:
                output_port = self.firedex_controller.output_port(shortest_path)

                priority = self.firedex_controller.build_priority("ARP")
                match = self.firedex_controller.build_match_arp(switch_identifier, input_port, dl_type, dl_src, dl_dst)
                actions = self.firedex_controller.build_actions(switch_identifier, output_port)
                self.firedex_controller.add_flow_rule(switch_identifier, priority, match, actions)

                self.send_packet_to_output_port(message, datapath, ofproto, parser, input_port, output_port)

        elif icmp_packet:
            nw_protocol = ipv4_packet.proto
            nw_src = ipv4_packet.src
            nw_dst = ipv4_packet.dst

            shortest_path = self.firedex_controller.shortest_path(switch_identifier, nw_dst)

            if shortest_path is None:
                self.flood_packet(message, datapath, ofproto, parser, input_port)
            else:
                output_port = self.firedex_controller.output_port(shortest_path)

                priority = self.firedex_controller.build_priority("ICMP")
                match = self.firedex_controller.build_match_icmp(switch_identifier, input_port, dl_type, nw_protocol, nw_src, nw_dst)
                actions = self.firedex_controller.build_actions(switch_identifier, output_port)
                self.firedex_controller.add_flow_rule(switch_identifier, priority, match, actions)

                self.send_packet_to_output_port(message, datapath, ofproto, parser, input_port, output_port)

        else:
            # flood
            self.flood_packet(message, datapath, ofproto, parser, input_port)

    def flood_packet(self, message, datapath, ofproto, parser, input_port):
        output_port = ofproto.OFPP_FLOOD
        self.send_packet_to_output_port(message, datapath, ofproto, parser, input_port, output_port)

    def send_packet_to_output_port(self, message, datapath, ofproto, parser, input_port, output_port):
        actions = [ parser.OFPActionOutput(output_port) ]

        buffer_identifier = message.buffer_id
        data = None
        if buffer_identifier == ofproto.OFP_NO_BUFFER:
            data = message.data

        output_packet = parser.OFPPacketOut(datapath = datapath, buffer_id = buffer_identifier, in_port = input_port, actions = actions, data = data)
        datapath.send_msg(output_packet)


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

from firedex.controller.firedex_controller import FiredexController
from firedex.controller.naming_utility import *


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
        message = event.msg
        datapath = message.datapath
        switch_identifier = switch_from_identifier(datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        input_port = message.match["in_port"]

        input_packet = packet.Packet(message.data)

        ethernet_packet = input_packet.get_protocol(ethernet.ethernet)
        dl_type = ethernet_packet.ethertype

        if dl_type == ether_types.ETH_TYPE_LLDP:
            return

        arp_packet = input_packet.get_protocol(arp.arp)
        ipv4_packet = input_packet.get_protocol(ipv4.ipv4)
        icmp_packet = input_packet.get_protocol(icmp.icmp)
        udp_packet = input_packet.get_protocol(udp.udp)
        tcp_packet = input_packet.get_protocol(tcp.tcp)

        if arp_packet:
            pass

        elif icmp_packet:
            pass

        elif udp_packet:
            pass

        elif tcp_packet:
            pass

        else:
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

        output_packet = parser.OFPPacketOut(
                                             datapath = datapath,
                                             buffer_id = buffer_identifier,
                                             in_port = input_port,
                                             actions = actions,
                                             data = data
                                           )
        datapath.send_msg(output_packet)

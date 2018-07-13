
import requests

from manager.flow_manager import FlowManager

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
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.topology import event

from utility.naming_utility import *


class FiredexApplication(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(FiredexApplication, self).__init__(*args, **kwargs)
        self.flow_manager = FlowManager()
        self.from_switch_identifier_to_switch_datapath = { }

    @set_ev_cls(event.EventSwitchEnter)
    def event_switch_enter(self, event_switch_enter):
        switch_datapath = event_switch_enter.switch.dp
        switch_identifier = switch_datapath.id
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_identifier)

        self.from_switch_identifier_to_switch_datapath[switch_identifier] = switch_datapath

    @set_ev_cls(event.EventSwitchLeave)
    def event_switch_leave(self, event_switch_leave):
        switch_datapath = event_switch_leave.switch.dp
        switch_identifier = switch_datapath.id
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_identifier)

        del self.from_switch_identifier_to_switch_datapath[switch_identifier]

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def on_packet_in(self, event):
        message = event.msg
        switch_datapath = message.datapath
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_datapath.id)
        ofproto = switch_datapath.ofproto
        parser = switch_datapath.ofproto_parser

        input_packet = packet.Packet(message.data)
        switch_input_port = message.match["in_port"]

        ethernet_packet = input_packet.get_protocol(ethernet.ethernet)

        dl_src = ethernet_packet.src
        dl_dst = ethernet_packet.dst
        dl_type = ethernet_packet.ethertype

        if dl_type == ether_types.ETH_TYPE_LLDP:
            return

        arp_packet = input_packet.get_protocol(arp.arp)
        ipv4_packet = input_packet.get_protocol(ipv4.ipv4)
        icmp_packet = input_packet.get_protocol(icmp.icmp)
        udp_packet = input_packet.get_protocol(udp.udp)
        tcp_packet = input_packet.get_protocol(tcp.tcp)

        if arp_packet:
            dl_src = arp_packet.src_mac  # source mac address
            dl_dst = arp_packet.dst_mac  # destionation mac address
            nw_src = arp_packet.src_ip  # source ip address
            nw_dst = arp_packet.dst_ip  # destination ip address

            output_port = self.output_port(switch_identifier, dl_dst)

            if output_port == "None":
                self.flood_packet(
                    message = message,
                    datapath = switch_datapath,
                    ofproto = ofproto,
                    parser = parser,
                    input_port = switch_input_port
                )
            else:
                self.send_packet_to_output_port(
                    message = message,
                    datapath = switch_datapath,
                    ofproto = ofproto,
                    parser = parser,
                    input_port = switch_input_port,
                    output_port = output_port
                )

        elif icmp_packet:
            nw_protocol = ipv4_packet.proto
            nw_src = ipv4_packet.src
            nw_dst = ipv4_packet.dst

            output_port = self.output_port(switch_identifier, dl_dst)

            if output_port == "None":
                self.flood_packet(
                    message=message,
                    datapath=switch_datapath,
                    ofproto=ofproto,
                    parser=parser,
                    input_port=switch_input_port
                )
            else:
                self.send_packet_to_output_port(
                    message=message,
                    datapath=switch_datapath,
                    ofproto=ofproto,
                    parser=parser,
                    input_port=switch_input_port,
                    output_port=output_port
                )

        elif udp_packet:
            pass

        elif tcp_packet:
            pass

        else:
            self.flood_packet(message, switch_datapath, ofproto, parser, switch_input_port)

    def output_port(self, source_identifier, destination_identifier):
        url = "http://127.0.0.1:8080/api/topology/output-port/%s/%s" % (source_identifier, destination_identifier)
        response = requests.get(url)
        content = response.json()
        output_port = content["output_port"]
        return output_port

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


import json

from manager.topology_manager import TopologyManager

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


class TopologyController(ControllerBase):

    def __init__(self, request, link, data, **configuration):
        super(TopologyController, self).__init__(request, link, data, **configuration)

    def topology(self, request, **kwargs):
        topology_manager = self.parent.registory["TopologyManager"]

        current_topology = topology_manager.topology()

        result = {
            "topology": current_topology
        }

        body = json.dumps(result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def output_port(self, request, **kwargs):
        topology_manager = self.parent.registory["TopologyManager"]

        source_identifier = request.json["source_identifier"]
        destination_identifier = request.json["destination_identifier"]

        output_port = topology_manager.output_port(
            source_identifier = source_identifier,
            destination_identifier = destination_identifier
        )

        result = {
            "from": source_identifier,
            "to": destination_identifier,
            "output_port": output_port
        }

        body = json.dumps(result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

    def output_port_to_ip_address(self, request, **kwargs):
        topology_manager = self.parent.registory["TopologyManager"]

        source_identifier = request.json["source_identifier"]
        destination_ip_address = request.json["destination_ip_address"]

        output_port = topology_manager.output_port_to_ip_address(
            source_identifier = source_identifier,
            destination_ip_address = destination_ip_address
        )

        result = {
            "from": source_identifier,
            "to": destination_ip_address,
            "output_port": output_port
        }

        body = json.dumps(result)

        response = Response(
            content_type = "application/json",
            body = body
        )

        return response

class TopologyApplication(app_manager.RyuApp):

    _CONTEXTS = {"wsgi": wsgi.WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(TopologyApplication, self).__init__(*args, **kwargs)
        self.topology_manager = TopologyManager()

        wsgi = kwargs['wsgi']
        wsgi.registory["TopologyManager"] = self.topology_manager

        mapper = wsgi.mapper

        mapper.connect(
            "Topology",
            "/api/topology/",
            controller = TopologyController,
            action = "topology",
            conditions = {"method": "GET"}
        )

        mapper.connect(
            "Output port",
            "/api/topology/output-port/",
            controller = TopologyController,
            action = "output_port",
            conditions = {"method": "POST"}
        )

        mapper.connect(
            "Output port to ip address",
            "/api/topology/output-port-to-ip-address/",
            controller = TopologyController,
            action = "output_port_to_ip_address",
            conditions = {"method": "POST"}
        )

    @set_ev_cls(event.EventSwitchEnter)
    def event_switch_enter(self, event_switch_enter):
        switch_datapath = event_switch_enter.switch.dp
        switch_identifier = switch_datapath.id
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_identifier)

        self.topology_manager.add_switch(
            switch_identifier = switch_identifier
        )

        print("add-switch: %s" % switch_identifier)

    @set_ev_cls(event.EventSwitchLeave)
    def event_switch_leave(self, event_switch_leave):
        switch_datapath = event_switch_leave.switch.dp
        switch_identifier = switch_datapath.id
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_identifier)

        self.topology_manager.remove_switch(
            switch_identifier = switch_identifier
        )

        print("remove-switch: %s" % switch_identifier)

    @set_ev_cls(event.EventLinkAdd)
    def event_link_add(self, event_link_add):
        switch_from_identifier = event_link_add.link.src.dpid
        switch_from_identifier = from_datapath_identifier_to_switch_identifier(switch_from_identifier)
        switch_to_identifier = event_link_add.link.dst.dpid
        switch_to_identifier = from_datapath_identifier_to_switch_identifier(switch_to_identifier)
        switch_from_port = event_link_add.link.src.port_no
        switch_to_port = event_link_add.link.dst.port_no

        self.topology_manager.add_link(
            node_from_identifier = switch_from_identifier,
            node_to_identifier = switch_to_identifier,
            node_from_port = switch_from_port,
            node_to_port = switch_to_port
        )

        print("add-link: %s %s" % (switch_from_identifier, switch_to_identifier))

    @set_ev_cls(event.EventLinkDelete)
    def event_link_delete(self, event_link_delete):
        switch_from_identifier = event_link_delete.link.src.dpid
        switch_from_identifier = from_datapath_identifier_to_switch_identifier(switch_from_identifier)
        switch_to_identifier = event_link_delete.link.dst.dpid
        switch_to_identifier = from_datapath_identifier_to_switch_identifier(switch_to_identifier)

        self.topology_manager.remove_link(
         node_from_identifier = switch_from_identifier,
         node_to_identifier = switch_to_identifier
        )

        print("remove-link: %s %s" % (switch_from_identifier, switch_to_identifier))

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def on_packet_in(self, event):
        message = event.msg
        switch_datapath = message.datapath
        switch_identifier = from_datapath_identifier_to_switch_identifier(switch_datapath.id)

        input_packet = packet.Packet(message.data)
        switch_input_port = message.match["in_port"]
        # switch_input_port = message.in_port

        ethernet_packet = input_packet.get_protocol(ethernet.ethernet)

        dl_src = ethernet_packet.src
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
            host_identifier = arp_packet.src_mac
            ip_address = arp_packet.src_ip

            self.__host_discovery(
                host_identifier = host_identifier,
                ip_address = ip_address,
                switch_identifier_connected_to = switch_identifier,
                switch_port_connected_to = switch_input_port
            )

        elif ipv4_packet:
            host_identifier = dl_src
            ip_address = ipv4_packet.src

            self.__host_discovery(
                host_identifier = host_identifier,
                ip_address = ip_address,
                switch_identifier_connected_to = switch_identifier,
                switch_port_connected_to = switch_input_port
            )

        elif ipv6_packet:
            pass

    def __host_discovery(self, host_identifier, ip_address, switch_identifier_connected_to, switch_port_connected_to):
        successful = self.topology_manager.add_host(
            host_identifier = host_identifier
        )

        if successful:
            self.topology_manager.update_host(
                host_identifier = host_identifier,
                ip_address = ip_address,
                switch_identifier_connected_to = switch_identifier_connected_to,
                switch_port_connected_to = switch_port_connected_to
            )

            self.topology_manager.add_link(
                node_from_identifier = host_identifier,
                node_to_identifier = switch_identifier_connected_to,
                node_from_port = 0,
                node_to_port = switch_port_connected_to
            )

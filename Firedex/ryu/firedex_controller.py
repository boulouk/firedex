# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from firedex.controller.firedex_message import *

from operator import attrgetter

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet.arp import arp
from ryu.lib.packet.icmp import icmp
from ryu.lib.packet.ipv4 import ipv4
from ryu.lib.packet.tcp import tcp
from ryu.lib.packet.udp import udp

class FiredexController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(FiredexController, self).__init__(*args, **kwargs)
        self.mac_to_port = { }
        self.datapaths = { }
        self.monitor_thread = hub.spawn(self._monitor)

        self.sleep = 10  # the interval of getting statistic
        self.ports_stat = { }
        self.ports_speed = { }

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(self.sleep)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body

        for stat in sorted(body, key=attrgetter('port_no')):
            if stat.port_no != ofproto_v1_3.OFPP_LOCAL:
                key = (ev.msg.datapath.id, stat.port_no)

                bytes_t_plus_1 = stat.tx_bytes

                if key not in self.ports_stat.keys():
                    self.ports_stat[key] = 0

                bytes_t = self.ports_stat[key]

                if key not in self.ports_speed.keys():
                    self.ports_speed[key] = 0

                speed = (bytes_t_plus_1 - bytes_t) / self.sleep
                self.ports_speed[key] = speed

                self.ports_stat[key] = bytes_t_plus_1

                print(ev.msg.datapath.id, " ", stat.port_no, " ", speed, " bytes/s")

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, event):
        datapath = event.datapath
        if event.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                print('Register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif event.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                print('Unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, event):
        pass

        # datapath = event.msg.datapath
        # ofproto = datapath.ofproto
        # parser = datapath.ofproto_parser

        # install table-miss flow entry
        # priority = 0
        # match = parser.OFPMatch()
        # actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        # self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, event):
        message = event.msg # packet-in message
        datapath = message.datapath # switch information
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        in_port = message.match['in_port']

        incoming_packet = packet.Packet(message.data)
        ethernet_packet = incoming_packet.get_protocol(ethernet.ethernet)

        if ethernet_packet.ethertype == ether_types.ETH_TYPE_LLDP:
            return # ignore lldp packet

        dl_type = ethernet_packet.ethertype
        dl_src = ethernet_packet.src
        dl_dst = ethernet_packet.dst

        datapath_id = datapath.id
        self.mac_to_port.setdefault(datapath_id, { })

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[datapath_id][dl_src] = in_port

        if dl_dst in self.mac_to_port[datapath_id]:
            out_port = self.mac_to_port[datapath_id][dl_dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        if out_port == ofproto.OFPP_FLOOD:
            actions = [parser.OFPActionOutput(out_port)]

            buffer_id = message.buffer_id
            data = None
            if message.buffer_id == ofproto.OFP_NO_BUFFER:
                data = message.data

            packet_out = parser.OFPPacketOut(datapath = datapath, buffer_id = buffer_id, in_port = in_port, actions = actions, data = data)
            datapath.send_msg(packet_out)

        elif out_port != ofproto.OFPP_FLOOD:
            arp_packet = incoming_packet.get_protocol(arp)
            ipv4_packet = incoming_packet.get_protocol(ipv4)
            icmp_packet = incoming_packet.get_protocol(icmp)
            udp_packet = incoming_packet.get_protocol(udp)
            tcp_packet = incoming_packet.get_protocol(tcp)

            firedex_message = None
            firedex_message_opposite = None

            if arp_packet:
                firedex_message = FiredexArp(datapath, message, in_port, out_port, dl_type, dl_src, dl_dst)
            elif icmp_packet:
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst

                firedex_message = FiredexIcmp(datapath, message, in_port, out_port, dl_type, dl_src, dl_dst, nw_protocol, nw_src, nw_dst)
            elif udp_packet:
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst
                tp_src = udp_packet.src_port
                tp_dst = udp_packet.dst_port
                firedex_message = FiredexUdp(datapath, message, in_port, out_port, dl_type, dl_src, dl_dst, nw_protocol, nw_src, nw_dst, tp_src, tp_dst)
                firedex_message_opposite = FiredexUdp(datapath, message, out_port, in_port, dl_type, dl_dst, dl_src, nw_protocol, nw_dst, nw_src, tp_dst, tp_src)

            elif tcp_packet:
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst
                tp_src = tcp_packet.src_port
                tp_dst = tcp_packet.dst_port

                firedex_message = FiredexTcp(datapath, message, in_port, out_port, dl_type, dl_src, dl_dst, nw_protocol, nw_src, nw_dst, tp_src, tp_dst)
                firedex_message_opposite = FiredexTcp(datapath, message, out_port, in_port, dl_type, dl_dst, dl_src, nw_protocol, nw_dst, nw_src, tp_dst, tp_src)

            if firedex_message is not None:
                firedex_message.handle()
            if firedex_message_opposite is not None:
                firedex_message_opposite.handle()

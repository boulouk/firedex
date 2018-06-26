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

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp
from ryu.lib.packet import icmp
from ryu.lib.packet import udp
from ryu.lib.packet import tcp

class Firedex(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    priority_service = {9000: 0, 9001: 1, 9002: 2, 9003: 3}
    drop_rate = {0: 0, 1: 1, 2: 2, 3: 3}

    def __init__(self, *args, **kwargs):
        super(Firedex, self).__init__(*args, **kwargs)
        self.mac_to_port = { }

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)

        print mod
        datapath.send_msg(mod)

    def add_group(self, datapath, group_id, out_port, queue):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        actions_drop = []
        actions_enqueue = [parser.OFPActionSetQueue(queue), parser.OFPActionOutput(out_port)]

        weight_drop = self.drop_rate[queue]
        weight_enqueue = 10 - weight_drop

        watch_port = ofproto_v1_3.OFPP_ANY
        watch_group = ofproto_v1_3.OFPQ_ALL

        bucket_drop = parser.OFPBucket(weight_drop, watch_port, watch_group, actions_drop)
        bucket_enqueue = parser.OFPBucket(weight_enqueue, watch_port, watch_group, actions_enqueue)

        buckets = [bucket_enqueue, bucket_drop]

        req = parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD, ofproto.OFPGT_SELECT, group_id, buckets)
        datapath.send_msg(req)

    def createOppositeUdp(self, datapath, message, in_port, out_port, dl_type, nw_protocol, dl_src, dl_dst, nw_src, nw_dst, tp_src, tp_dst):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(in_port=in_port, eth_type=dl_type, ip_proto=nw_protocol,
                                eth_src=dl_src, eth_dst=dl_dst, ipv4_src=nw_src, ipv4_dst=nw_dst,
                                udp_src=tp_src, udp_dst=tp_dst)

        actions = [parser.OFPActionOutput(out_port)]

        queue = self.priority_service.get(tp_src)
        if queue != None:
            n_queues = 4
            group_id = queue + (out_port - 1) * n_queues
            self.add_group(datapath, group_id, out_port, queue)
            actions = [parser.OFPActionGroup(group_id)]

        if message.buffer_id != ofproto.OFP_NO_BUFFER:
            self.add_flow(datapath, 1, match, actions, message.buffer_id)
            return
        else:
            self.add_flow(datapath, 1, match, actions)

    def createOppositeTcp(self, datapath, message, in_port, out_port, dl_type, nw_protocol, dl_src, dl_dst, nw_src, nw_dst, tp_src, tp_dst):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(in_port=in_port, eth_type=dl_type, ip_proto=nw_protocol,
                                eth_src=dl_src, eth_dst=dl_dst, ipv4_src=nw_src, ipv4_dst=nw_dst,
                                tcp_src=tp_src, tcp_dst=tp_dst)

        actions = [parser.OFPActionOutput(out_port)]

        queue = self.priority_service.get(tp_src)
        print queue
        if queue != None:
            n_queues = 4
            group_id = queue + (out_port - 1) * n_queues
            self.add_group(datapath, group_id, out_port, queue)
            actions = [parser.OFPActionGroup(group_id)]

        if message.buffer_id != ofproto.OFP_NO_BUFFER:
            self.add_flow(datapath, 1, match, actions, message.buffer_id)
            return
        else:
            self.add_flow(datapath, 1, match, actions)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, event):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if event.msg.msg_len < event.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes", event.msg.msg_len, event.msg.total_len)

        message = event.msg
        datapath = message.datapath
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

        actions = [parser.OFPActionOutput(out_port)]

        if out_port != ofproto.OFPP_FLOOD:
            print "NOT_FLOOD"
            print out_port
            arp_packet = incoming_packet.get_protocol(arp.arp)
            ipv4_packet = incoming_packet.get_protocol(ipv4.ipv4)
            icmp_packet = incoming_packet.get_protocol(icmp.icmp)
            udp_packet = incoming_packet.get_protocol(udp.udp)
            tcp_packet = incoming_packet.get_protocol(tcp.tcp)

            if arp_packet:
                print "ARP"
                match = parser.OFPMatch(in_port=in_port, eth_type=dl_type, eth_src=dl_src, eth_dst=dl_dst)

            elif icmp_packet:
                print "ICMP"
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst
                match = parser.OFPMatch(in_port=in_port, eth_type=dl_type, ip_proto=nw_protocol,
                                        eth_src=dl_src, eth_dst=dl_dst, ipv4_src=nw_src, ipv4_dst=nw_dst)

            elif udp_packet:
                print "UDP"
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst
                tp_src = udp_packet.src_port
                tp_dst = udp_packet.dst_port
                match = parser.OFPMatch(in_port=in_port, eth_type=dl_type, ip_proto=nw_protocol,
                                        eth_src=dl_src, eth_dst=dl_dst, ipv4_src=nw_src, ipv4_dst=nw_dst,
                                        udp_src=tp_src, udp_dst=tp_dst)

                self.createOppositeUdp(datapath, message, out_port, in_port, dl_type, nw_protocol, dl_dst, dl_src, nw_dst, nw_src, tp_dst, tp_src)

                queue = self.priority_service.get(tp_dst)
                if queue != None:
                    n_queues = 4
                    group_id = queue + (out_port - 1) * n_queues
                    self.add_group(datapath, group_id, out_port, queue)
                    actions = [parser.OFPActionGroup(group_id)]

            elif tcp_packet:
                print "TCP"
                nw_protocol = ipv4_packet.proto
                nw_src = ipv4_packet.src
                nw_dst = ipv4_packet.dst
                tp_src = tcp_packet.src_port
                tp_dst = tcp_packet.dst_port
                match = parser.OFPMatch(in_port=in_port, eth_type=dl_type, ip_proto=nw_protocol,
                                        eth_src=dl_src, eth_dst=dl_dst, ipv4_src=nw_src, ipv4_dst=nw_dst,
                                        tcp_src=tp_src, tcp_dst=tp_dst)

                self.createOppositeTcp(datapath, message, out_port, in_port, dl_type, nw_protocol, dl_dst, dl_src, nw_dst, nw_src, tp_dst, tp_src)

                queue = self.priority_service.get(tp_dst)
                if queue != None:
                    n_queues = 4
                    group_id = queue + (out_port - 1) * n_queues
                    self.add_group(datapath, group_id, out_port, queue)
                    actions = [parser.OFPActionGroup(group_id)]

            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if message.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, message.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)

        data = None
        if message.buffer_id == ofproto.OFP_NO_BUFFER:
            data = message.data

        packet_out = parser.OFPPacketOut(datapath=datapath, buffer_id=message.buffer_id, in_port=in_port, actions=actions, data=data)
        datapath.send_msg(packet_out)
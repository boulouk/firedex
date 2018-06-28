
from ryu.ofproto import ofproto_v1_3

priority_service = {9000: 0, 9001: 1, 9002: 2, 9003: 3}
drop_rate = {0: 0, 1: 2, 2: 4, 3: 8}

class FiredexMessage:

    def __init__(self, datapath, message, in_port, out_port):
        self.datapath = datapath
        self.message = message
        self.in_port = in_port
        self.out_port = out_port

    def add_flow(self, datapath, priority, match, actions, buffer_id = None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        instructions = [ parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions) ]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath = datapath, buffer_id = buffer_id, priority = priority, match = match, instructions = instructions)
        else:
            mod = parser.OFPFlowMod(datapath = datapath, priority = priority, match = match, instructions = instructions)

        datapath.send_msg(mod)

    def add_group(self, datapath, group_id, out_port, queue):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        actions_drop = [ ]
        actions_enqueue = [ parser.OFPActionSetQueue(queue), parser.OFPActionOutput(out_port) ]

        weight_drop = drop_rate[queue]
        weight_enqueue = 10 - weight_drop

        watch_port = ofproto_v1_3.OFPP_ANY
        watch_group = ofproto_v1_3.OFPQ_ALL

        bucket_drop = parser.OFPBucket(weight_drop, watch_port, watch_group, actions_drop)
        bucket_enqueue = parser.OFPBucket(weight_enqueue, watch_port, watch_group, actions_enqueue)

        buckets = [ bucket_enqueue, bucket_drop ]

        group = parser.OFPGroupMod(datapath, ofproto.OFPGC_ADD, ofproto.OFPGT_SELECT, group_id, buckets)
        datapath.send_msg(group)

class FiredexArp(FiredexMessage):

    def __init__(self, datapath, message, in_port, out_port, dl_type, dl_src, dl_dst):
        FiredexMessage.__init__(self, datapath, message, in_port, out_port)
        self.dl_type = dl_type
        self.dl_src = dl_src
        self.dl_dst = dl_dst

        print("ARP (in:{}, out:{}, mac:({}, {}))".format(in_port, out_port, dl_src, dl_dst))

    def handle(self):
        datapath = self.datapath
        message = self.message
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        priority = 1
        match = self.match()
        actions = self.actions()
        in_port = self.in_port
        buffer_id = message.buffer_id

        if message.buffer_id != ofproto.OFP_NO_BUFFER:
            self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions, buffer_id = message.buffer_id)
            return

        self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions)

        data = message.data
        packet_out = parser.OFPPacketOut(datapath = datapath, buffer_id = buffer_id, in_port = in_port, actions = actions, data = data)
        datapath.send_msg(packet_out)

    def match(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(in_port = self.in_port, eth_type = self.dl_type, eth_src = self.dl_src, eth_dst = self.dl_dst)
        return match

    def actions(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser
        actions = [ parser.OFPActionOutput(self.out_port) ]
        return actions

class FiredexIcmp(FiredexMessage):

    def __init__(self, datapath, message, in_port, out_port, dl_type, dl_src, dl_dst, nw_protocol, nw_src, nw_dst):
        FiredexMessage.__init__(self, datapath, message, in_port, out_port)
        self.dl_type = dl_type
        self.dl_src = dl_src
        self.dl_dst = dl_dst
        self.nw_protocol = nw_protocol
        self.nw_src = nw_src
        self.nw_dst = nw_dst

        print("ICMP (in:{}, out:{}, mac:({}, {}), ip:({}, {}))".format(in_port, out_port, dl_src, dl_dst, nw_src, nw_dst))

    def handle(self):
        datapath = self.datapath
        message = self.message
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        priority = 1
        match = self.match()
        actions = self.actions()
        in_port = self.in_port
        buffer_id = message.buffer_id

        if message.buffer_id != ofproto.OFP_NO_BUFFER:
            self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions, buffer_id = message.buffer_id)
            return

        self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions)

        data = message.data
        packet_out = parser.OFPPacketOut(datapath = datapath, buffer_id = buffer_id, in_port = in_port, actions = actions, data = data)
        datapath.send_msg(packet_out)

    def match(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(in_port = self.in_port, eth_type = self.dl_type, eth_src = self.dl_src, eth_dst = self.dl_dst,
                                ip_proto = self.nw_protocol, ipv4_src = self.nw_src, ipv4_dst = self.nw_dst)
        return match

    def actions(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser
        actions = [ parser.OFPActionOutput(self.out_port) ]
        return actions

class FiredexUdp(FiredexMessage):

    def __init__(self, datapath, message, in_port, out_port, dl_type, dl_src, dl_dst, nw_protocol, nw_src, nw_dst, tp_src, tp_dst):
        FiredexMessage.__init__(self, datapath, message, in_port, out_port)
        self.dl_type = dl_type
        self.dl_src = dl_src
        self.dl_dst = dl_dst
        self.nw_protocol = nw_protocol
        self.nw_src = nw_src
        self.nw_dst = nw_dst
        self.tp_src = tp_src
        self.tp_dst = tp_dst

        print("UDP (in:{}, out:{}, mac:({}, {}), ip:({}, {}), tp:({}, {}))".format(in_port, out_port, dl_src, dl_dst, nw_src, nw_dst, tp_src, tp_dst))

    def handle(self):
        datapath = self.datapath
        message = self.message
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        priority = 1
        match = self.match()
        actions = self.actions()
        in_port = self.in_port
        buffer_id = message.buffer_id

        if message.buffer_id != ofproto.OFP_NO_BUFFER:
            self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions, buffer_id = message.buffer_id)
            return

        self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions)

        data = message.data
        packet_out = parser.OFPPacketOut(datapath = datapath, buffer_id = buffer_id, in_port = in_port, actions = actions, data = data)
        datapath.send_msg(packet_out)

    def match(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(in_port = self.in_port, eth_type = self.dl_type, eth_src = self.dl_src, eth_dst = self.dl_dst,
                                ip_proto = self.nw_protocol, ipv4_src = self.nw_src, ipv4_dst = self.nw_dst,
                                udp_src = self.tp_src, udp_dst = self.tp_dst)
        return match

    def actions(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser

        actions = [ parser.OFPActionOutput(self.out_port) ]

        queue = priority_service.get(self.tp_dst)
        if queue is not None:
            n_queues = priority_service.__len__()
            group_id = queue + (self.out_port - 1) * n_queues
            self.add_group(datapath, group_id, self.out_port, queue)
            actions = [ parser.OFPActionGroup(group_id) ]

        return actions

class FiredexTcp(FiredexMessage):

    def __init__(self, datapath, message, in_port, out_port, dl_type, dl_src, dl_dst, nw_protocol, nw_src, nw_dst, tp_src, tp_dst):
        FiredexMessage.__init__(self, datapath, message, in_port, out_port)
        self.dl_type = dl_type
        self.dl_src = dl_src
        self.dl_dst = dl_dst
        self.nw_protocol = nw_protocol
        self.nw_src = nw_src
        self.nw_dst = nw_dst
        self.tp_src = tp_src
        self.tp_dst = tp_dst

        print("TCP (in:{}, out:{}, mac:({}, {}), ip:({}, {}), tp:({}, {}))".format(in_port, out_port, dl_src, dl_dst, nw_src, nw_dst, tp_src, tp_dst))

    def handle(self):
        datapath = self.datapath
        message = self.message
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        priority = 1
        match = self.match()
        actions = self.actions()
        in_port = self.in_port
        buffer_id = message.buffer_id

        if message.buffer_id != ofproto.OFP_NO_BUFFER:
            self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions, buffer_id = message.buffer_id)
            return

        self.add_flow(datapath = datapath, priority = priority, match = match, actions = actions)

        data = message.data
        packet_out = parser.OFPPacketOut(datapath = datapath, buffer_id = buffer_id, in_port = in_port, actions = actions, data = data)
        datapath.send_msg(packet_out)

    def match(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(in_port = self.in_port, eth_type = self.dl_type, eth_src = self.dl_src, eth_dst = self.dl_dst,
                                ip_proto = self.nw_protocol, ipv4_src = self.nw_src, ipv4_dst = self.nw_dst,
                                tcp_src = self.tp_src, tcp_dst = self.tp_dst)
        return match

    def actions(self):
        datapath = self.datapath
        parser = datapath.ofproto_parser

        actions = [parser.OFPActionOutput(self.out_port)]

        queue = priority_service.get(self.tp_dst)
        if queue is not None:
            n_queues = priority_service.__len__()
            group_id = queue + (self.out_port - 1) * n_queues
            self.add_group(datapath, group_id, self.out_port, queue)
            actions = [parser.OFPActionGroup(group_id)]

        return actions

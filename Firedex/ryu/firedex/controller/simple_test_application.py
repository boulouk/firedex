
import os

from ryu.base import app_manager
from ryu.cmd import manager
from ryu.lib import hub

from time import sleep


application_name = "FiredexApplication"

class SimpleTestApplication(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(SimpleTestApplication, self).__init__(*args, **kwargs)
        self.monitor_thread = hub.spawn(self.__run_test)

    def __run_test(self):
        application_manager = manager.AppManager.get_instance()

        firedex_application = None
        firedex_initialized = False

        while not firedex_initialized:
            applications = application_manager.applications
            if application_name in applications.keys():
                firedex_application = applications[application_name]
                firedex_initialized = True
            else:
                sleep(1)

        assert (firedex_application is not None)

        firedex_controller = firedex_application.get_firedex_controller()
        assert (firedex_controller is not None)

        sleep(3)

        # ARP
        switch_identifier = "S2"
        packet_type = "ARP"
        priority = firedex_controller.build_priority(packet_type)
        input_port = 1
        match_parameters = {"dl_src": "00:00:00:00:00:01", "dl_dst": "00:00:00:00:00:02"}
        match = firedex_controller.build_match(switch_identifier, packet_type, input_port, match_parameters)
        action_parameters = [ ("OUTPUT", 2) ]
        actions = firedex_controller.build_actions(switch_identifier, action_parameters)
        firedex_controller.build_flow_rule(switch_identifier, priority, match, actions)

        # ICMP
        switch_identifier = "S2"
        packet_type = "ICMP"
        priority = firedex_controller.build_priority(packet_type)
        input_port = 2
        match_parameters = {"nw_src": "10.0.0.2", "nw_dst": "10.0.0.1"}
        match = firedex_controller.build_match(switch_identifier, packet_type, input_port, match_parameters)
        action_parameters = [ "DROP" ]
        actions = firedex_controller.build_actions(switch_identifier, action_parameters)
        firedex_controller.build_flow_rule(switch_identifier, priority, match, actions)

        # UDP
        switch_identifier = "S2"
        packet_type = "UDP"
        priority = firedex_controller.build_priority(packet_type)
        input_port = 1
        match_parameters = {"nw_src": "10.0.0.2", "nw_dst": "10.0.0.1", "tp_src": 8888, "tp_dst": 8889}
        match = firedex_controller.build_match(switch_identifier, packet_type, input_port, match_parameters)
        action_parameters = [ ("SET-QUEUE", 2) ]
        actions = firedex_controller.build_actions(switch_identifier, action_parameters)
        firedex_controller.build_flow_rule(switch_identifier, priority, match, actions)

        # GROUP
        switch_identifier = "S2"
        group_type = "SELECT"
        group_identifier = 2
        actions_bucket1 = firedex_controller.build_actions(switch_identifier, [ ("SET-QUEUE", 2), ("OUTPUT", 2) ])
        actions_bucket2 = firedex_controller.build_actions(switch_identifier, [ "DROP" ])
        bucket1 = firedex_controller.build_bucket(switch_identifier, actions_bucket1, 5)
        bucket2 = firedex_controller.build_bucket(switch_identifier, actions_bucket2, 5)
        buckets = [ bucket1, bucket2 ]
        firedex_controller.build_group(switch_identifier, group_type, group_identifier, buckets)

        # TCP
        switch_identifier = "S2"
        packet_type = "TCP"
        priority = firedex_controller.build_priority(packet_type)
        input_port = 2
        match_parameters = {"nw_src": "10.0.0.2", "nw_dst": "10.0.0.1", "tp_src": 8889, "tp_dst": 8888}
        match = firedex_controller.build_match(switch_identifier, packet_type, input_port, match_parameters)
        action_parameters = [ ("GROUP", 2) ]
        actions = firedex_controller.build_actions(switch_identifier, action_parameters)
        firedex_controller.build_flow_rule(switch_identifier, priority, match, actions)

        print("Test completed (check the rules through OVS).")

        sleep(1)

        os._exit(0)

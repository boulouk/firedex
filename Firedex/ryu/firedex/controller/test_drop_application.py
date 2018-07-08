
import os

from ryu.base import app_manager
from ryu.cmd import manager
from ryu.lib import hub

from time import sleep


application_name = "FiredexApplication"

class DropTestApplication(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(DropTestApplication, self).__init__(*args, **kwargs)
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

        # ICMP
        switch_identifier = "S1"
        group_type = "SELECT"
        group_identifier = 1
        drop_weight = 5
        drop_enqueue = 5
        drop_actions = firedex_controller.build_actions(switch_identifier, ["DROP"])
        enqueue_actions = firedex_controller.build_actions(  switch_identifier, [ ("SET-QUEUE", 2), ("OUTPUT", 2) ]  )
        drop_bucket = firedex_controller.build_bucket(switch_identifier, drop_actions, drop_weight)
        enqueue_bucket = firedex_controller.build_bucket(switch_identifier, enqueue_actions, drop_weight)
        buckets = [ drop_bucket, enqueue_bucket ]
        firedex_controller.build_group(switch_identifier, group_type, group_identifier, buckets)

        switch_identifier = "S1"
        packet_type = "ICMP"
        priority = firedex_controller.build_priority(packet_type)
        input_port = 1
        match_parameters = {"nw_src": "10.0.0.1", "nw_dst": "10.0.0.2"}
        match = firedex_controller.build_match(switch_identifier, packet_type, input_port, match_parameters)
        action_parameters = [("GROUP", 1)]
        actions = firedex_controller.build_actions(switch_identifier, action_parameters)
        firedex_controller.build_flow_rule(switch_identifier, priority, match, actions)

        switch_identifier = "S1"
        packet_type = "ICMP"
        priority = firedex_controller.build_priority(packet_type)
        input_port = 2
        match_parameters = {"nw_src": "10.0.0.2", "nw_dst": "10.0.0.1"}
        match = firedex_controller.build_match(switch_identifier, packet_type, input_port, match_parameters)
        action_parameters = [("OUTPUT", 1)]
        actions = firedex_controller.build_actions(switch_identifier, action_parameters)
        firedex_controller.build_flow_rule(switch_identifier, priority, match, actions)

        print("Test completed (execute ping on mininet).")

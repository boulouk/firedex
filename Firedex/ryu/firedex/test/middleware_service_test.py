
import os as system
from firedex.controller.firedex_main import run_controller_asynchronously
from ryu.cmd import manager
from ryu.lib.packet import ether_types
from time import sleep


application_name = "FiredexApplication"

def run_test():
    run_controller_asynchronously()
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

    sleep(5)

    # switch_identifier = "S2"
    # flow_type = "ARP"
    # priority = firedex_controller.build_priority(flow_type)
    # match = firedex_controller.build_match(switch_identifier, 1, ether_types.ETH_TYPE_ARP, "10.0.0.2", "10.0.0.3")
    # actions = firedex_controller.build_actions(switch_identifier, 2)
    # firedex_controller.add_flow_rule(switch_identifier, priority, match, actions)

    sleep(5)

    system._exit(0)


if __name__ == '__main__':
    run_test()

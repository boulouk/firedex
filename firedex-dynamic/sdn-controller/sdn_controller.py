
from ryu.cmd import manager

APPLICATIONS = [ "topology_application", "flow_application" ]

def run_sdn_controller(applications):
    arguments = []

    arguments.extend(applications)
    arguments.append("--observe-links")
    arguments.append("--verbose")
    arguments.append("--enable-debugger")

    manager.main( args = arguments )


if __name__ == '__main__':
    run_sdn_controller(applications = APPLICATIONS)

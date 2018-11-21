
from ryu.cmd import manager


applications = ["topology_application", "flow_application"]

def run_controller(applications):
    arguments = []
    arguments.extend(applications)
    arguments.append("--observe-links")
    arguments.append("--enable-debugger")
    manager.main( args = arguments )


if __name__ == '__main__':
    run_controller(applications = applications)


import threading


def run_controller(applications):
    from ryu.cmd import manager

    arguments = []
    arguments.extend(applications)
    arguments.append("--observe-links")
    arguments.append("--enable-debugger")
    manager.main( args = arguments)

def run_controller_asynchronously(applications):
    controller_thread = threading.Thread(target = run_controller, args = (applications, ))
    controller_thread.start()


if __name__ == '__main__':
    # run_controller( ["firedex_application"] )
    run_controller( ["firedex_application", "test_mininet_application"] )


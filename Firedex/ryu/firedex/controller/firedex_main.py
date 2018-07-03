
import sys as system
import threading

from ryu.cmd import manager


def run_controller(applications):
    for application in applications:
        system.argv.append(application)
    system.argv.append('--observe-links') # enable topology service
    system.argv.append('--enable-debugger') # enable debugging
    manager.main()

def run_controller_asynchronously(applications):
    controller_thread = threading.Thread(target = run_controller, args = (applications, ))
    controller_thread.start()


if __name__ == '__main__':
    # run_controller( ["firedex_application"] )
    # run_controller( ["firedex_application", "simple_test_application"] )
    run_controller( ["firedex_application", "mininet_test_application"] )


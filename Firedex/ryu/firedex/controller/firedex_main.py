
import sys as system
from ryu.cmd import manager
from threading import Thread


def run_controller():
    system.argv.append('firedex_application') # load firedex application
    system.argv.append('--observe-links') # enable topology service
    system.argv.append('--enable-debugger') # enable debugging
    manager.main()

def run_controller_asynchronously():
    controller_thread = Thread(target = run_controller)
    controller_thread.start()


if __name__ == '__main__':
    run_controller()



import os

from firedex.controller.firedex_main import *

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch

from single_switch_topology import SingleSwitchTopology

from time import sleep


def run_experiment():
    topology = SingleSwitchTopology(2)
    network = Mininet(
                       topology,
                       controller = RemoteController("ryu-controller"),
                       switch = OVSSwitch,
                       autoSetMacs = True,
                       autoStaticArp = True
                     )

    network.start()

    sleep(3)

    run_controller_asynchronously( ["firedex_application", "test_mininet_application"] )

    sleep(10)

    network.pingAll()

    sleep(3)

    network.stop()

    os._exit(0)


if __name__ == '__main__':
    run_experiment()

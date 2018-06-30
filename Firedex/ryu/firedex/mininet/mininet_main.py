
from mininet.net import Mininet
from mininet.log import setLogLevel

from mininet_topology import SingleSwitchTopology

def run_test():
    topology = SingleSwitchTopology(n = 3)
    network = Mininet(topology, cleanup = True, autoSetMacs = True)
    network.start()
    network.pingAll()
    network.stop()


if __name__ == '__main__':
    setLogLevel("info")
    run_test()


from mininet.topo import Topo
from firedex.controller.naming_utility import *

class SingleSwitchTopology(Topo):

    def build(self, n = 2):
        switch_identifier = switch_from_identifier(1)
        switch = self.addSwitch(switch_identifier)

        for i in range(n):
            host_identifier = host_from_identifier(i + 1)
            host = self.addHost(host_identifier)
            self.addLink(host, switch)

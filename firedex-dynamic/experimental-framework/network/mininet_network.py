
import os
import signal
import subprocess

from mininet_topology import MininetTopology
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCIntf

class MininetNetwork:

    def __init__(self, bandwidth, delay, error_rate):
        self.__publishers_switch = "s1"
        self.__subscribers_switch = "s2"
        self.__dummy_switch = "s254"
        self.__switch_protocols = "OpenFlow13"

        self.__bandwidth = bandwidth
        self.__delay = delay
        self.__error_rate = error_rate

        self.__hosts = []

        self.__network = Mininet()
        self.__host_processes = []

    def add_host(self, name, host):
        self.__hosts.append( { "name": name, "ip": host } )

    def host_by_name(self, name):
        for host in self.__network.hosts:
            if host.name == name:
                return host
        return None

    def start(self):
        topology = MininetTopology()

        topology.addSwitch(
            name = self.__publishers_switch,
            protocols = self.__switch_protocols
        )

        topology.addSwitch(
            name = self.__subscribers_switch,
            protocols = self.__switch_protocols
        )

        topology.addSwitch(
            name = self.__dummy_switch,
            protocols = self.__switch_protocols
        )

        topology.addLink(
            node1 = self.__publishers_switch,
            node2 = self.__dummy_switch
        )

        topology.addLink(
            node1 = self.__subscribers_switch,
            node2 = self.__dummy_switch
        )

        for host in self.__hosts:
            topology.addHost(
                name = host["name"],
                ip = host["ip"]
            )

            if host["name"] == "broker":
                topology.addLink(
                    node1 = host["name"],
                    node2 = self.__dummy_switch
                )
            elif host["name"].startswith("pub"):
                topology.addLink(
                    node1 = host["name"],
                    node2 = self.__publishers_switch
                )
            elif host["name"].startswith("sub"):
                topology.addLink(
                    node1 = host["name"],
                    node2 = self.__subscribers_switch,
                    # intf = TCIntf,
                    # params1 = {'delay': str(self.__latency) + "ms"},
                    # params2 = {'delay': str(0) + "ms"}
                )

        self.__network = Mininet(
            topo = topology,
            controller = RemoteController,
            waitConnected = True,
            autoSetMacs = True,
            autoStaticArp = True
        )

        self.__network.addNAT().configDefault()

        self.__network.start()

    def priority_queues(self, priorities):
        bandwidth = self.__bandwidth * 8

        command = "sudo ovs-vsctl"
        command += " -- set port %s-eth2 qos=@newqos -- " % self.__dummy_switch
        command += "--id=@newqos create qos type=linux-htb other-config:min-rate=%s other-config:max-rate=%s " % \
                   ( str(0), str(bandwidth) )
        command += "queues="
        for priority in range(1, priorities + 1):
            queue_name = str(priority)
            queue_identifier = "@q%s" % queue_name
            command += "%s=%s," % (queue_name, queue_identifier)
        command = command[:-1]
        command += " -- "
        for priority in range(1, priorities + 1):
            queue_name = str(priority)
            queue_identifier = "@q%s" % queue_name
            command += "--id=%s create queue other-config:priority=%s other-config:min-rate=%s other-config:max-rate=%s -- " % \
                       ( queue_identifier, str(priority), str(0), str(bandwidth) )

        process = subprocess.Popen(
            command,
            shell = True,
            stdin = open(os.devnull),
            stdout = open(os.devnull),
            stderr = open(os.devnull)
        )

        process.wait()

    def topology_discovery(self):
        self.__network.pingAll()

    def execute(self, name, command):
        host = self.host_by_name(name)
        process = host.popen(command, shell = True)
        self.__host_processes.append( (name, process) )

    def stop(self):
        for host_process in self.__host_processes:
            try:
                process = host_process[1]
                os.killpg(process.pid, signal.SIGTERM)
            except Exception:
                pass

        self.__host_processes = []
        self.__network.stop()

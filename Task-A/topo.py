#!/usr/bin/env python3
from mininet.node import Controller, OVSSwitch
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.topo import Topo

class AssignmentTopo(Topo):
    def build(self):
        # add the switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        # add hosts with IPs
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        dns = self.addHost('dns', ip='10.0.0.5/24')
        # nat = self.addNode('nat0', cls=NAT, ip='10.0.0.254/24', inNamespace=False)
        # links
        self.addLink(h1, s1, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h2, s2, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h3, s3, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h4, s4, cls=TCLink, bw=100, delay='2ms')
        # links between switches and dns
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='5ms')
        self.addLink(s2, s3, cls=TCLink, bw=100, delay='8ms')
        self.addLink(s3, s4, cls=TCLink, bw=100, delay='10ms')
        self.addLink(dns, s2, cls=TCLink, bw=100, delay='1ms')
        # self.addLink(s2, nat)

def run():
    topo = AssignmentTopo()
    net = Mininet(topo=topo, controller=Controller, link=TCLink, switch=OVSSwitch, autoSetMacs=True)
    net.start()
    dns = net.get('dns')
    dns.cmd('ip addr add 10.0.2.1/24 dev dns-eth0')
    print("\nNetwork started.\n")
    net.pingAll()
    print("\nStarting Mininet\n")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()

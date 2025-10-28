#!/usr/bin/python3

from mininet.net import Mininet
from mininet.node import Host, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def setup_network():
    net = Mininet(
        controller=None,  # No controller used
        switch=OVSKernelSwitch,
        host=Host,
        link=TCLink
    )

    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    dns = net.addHost('dns', ip='10.0.0.5/24')  # Custom DNS resolver

    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
    s3 = net.addSwitch('s3', failMode='standalone')
    s4 = net.addSwitch('s4', failMode='standalone')

    info('Using NAT for external connectivity\n')
    nat = net.addNAT(ip='10.0.0.254/24', inNamespace=False, connect=False)
    net.addLink(nat, s1)
    # Connect each host to its respective switch
    net.addLink(h1, s1, bw=100, delay='2ms')
    net.addLink(h2, s2, bw=100, delay='2ms')
    net.addLink(h3, s3, bw=100, delay='2ms')
    net.addLink(h4, s4, bw=100, delay='2ms')
    net.addLink(dns, s2, bw=100, delay='1ms')
    # Interconnecting the switches
    net.addLink(s1, s2, bw=100, delay='5ms')
    net.addLink(s2, s3, bw=100, delay='8ms')
    net.addLink(s3, s4, bw=100, delay='10ms')

    info('Booting up network\n')
    net.start()
    for host in [h1, h2, h3, h4, dns]:
        host.cmd(f'ip route add default via 10.0.0.254')

    info('Applying custom DNS setup for hosts\n')
    for host in [h1, h2, h3, h4]:
        host.cmd('rm /etc/resolv.conf')
        host.cmd(f'echo "nameserver 10.0.0.5" > /etc/resolv.conf')
        info(f"DNS for {host.name} set to 10.0.0.5\n")

    info('*** Launching Custom DNS Resolver on 10.0.0.5\n')
    dns.cmd('sudo python3 cr.py &')
    info('DNS Resolver operational\n')
    info('Launching CLI\n')
    CLI(net)
    info('Shutting down network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setup_network()

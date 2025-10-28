#!/usr/bin/python3
"""
creates the Mininet topology, configures clients to use the
custom resolver, and launches the resolver script.
"""
from mininet.net import Mininet
from mininet.node import Host, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def build_dns_topology():
    """Initializes and configures the Mininet network for the DNS."""
    net = Mininet(controller=None, switch=OVSKernelSwitch, host=Host, link=TCLink)
    info('--> Creating network hosts...\n')
    client1 = net.addHost('h1', ip='10.0.0.1/24')
    client2 = net.addHost('h2', ip='10.0.0.2/24')
    client3 = net.addHost('h3', ip='10.0.0.3/24')
    client4 = net.addHost('h4', ip='10.0.0.4/24')
    resolver_node = net.addHost('dns', ip='10.0.0.5/24') # Host for our Python resolver
    info('--> Creating network switches...\n')
    s1 = net.addSwitch('s1', failMode='standalone')
    s2 = net.addSwitch('s2', failMode='standalone')
    s3 = net.addSwitch('s3', failMode='standalone')
    s4 = net.addSwitch('s4', failMode='standalone')
    info('--> Configuring NAT for Internet connectivity...\n')
    # macOS users: Find your interface with `ifconfig` (e.g., 'en0' for Wi-Fi).
    # Linux users: Use `ip a` (e.g., 'enp0s3' or 'eth0').
    nat_gateway = net.addNAT(ip='10.0.0.254/24', inNamespace=False, nat_iface='wlan0', connect=False)
    info('--> Establishing network links...\n')
    net.addLink(nat_gateway, s1) 
    net.addLink(client1, s1, bw=100, delay='2ms')
    net.addLink(client2, s2, bw=100, delay='2ms')
    net.addLink(client3, s3, bw=100, delay='2ms')
    net.addLink(client4, s4, bw=100, delay='2ms')
    net.addLink(resolver_node, s2, bw=100, delay='1ms')
    net.addLink(s1, s2, bw=100, delay='5ms')
    net.addLink(s2, s3, bw=100, delay='8ms')
    net.addLink(s3, s4, bw=100, delay='10ms')

    info('--> Starting network services...\n')
    net.start()

    info('--> Configuring default routes for all hosts...\n')
    all_hosts = [client1, client2, client3, client4, resolver_node]
    for host in all_hosts:
        host.cmd(f'ip route add default via 10.0.0.254')
    info('--> Pointing clients to the custom DNS resolver...\n')
    for host in [client1, client2, client3, client4]:
        # configuration for internet 
        # overwrites /etc/resolv.conf to use our resolver at 10.0.0.5
        host.cmd(f'echo "nameserver 10.0.0.5" > /etc/resolv.conf')
        info(f'---> DNS for {host.name} set to 10.0.0.5\n')
    info('--> Launching the custom DNS resolver on host "dns"...\n')
    # run the resolver in the background (&) on the 'dns' node
    resolver_node.cmd('sudo python3 cr.py > /tmp/resolver.log 2>&1 &')
    info('--> Resolver script is now running.\n')
    info('--> Mininet CLI is ready.\n')
    CLI(net)
    info('--> Shutting down network.\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    build_dns_topology()

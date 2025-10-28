#!/usr/bin/env python3
from mininet.net import Mininet, NAT
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.topo import Topo

class AssignmentTopo(Topo):
    def build(self):
        # Add the switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        
        # Add hosts with IPs
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        # --- FIX 1: Corrected H2 IP to match diagram ---
        h2 = self.addHost('h2', ip='10.0.0.2/24') 
        h3 = self.addHost('h3', ip='10.0.0.3/24')
        h4 = self.addHost('h4', ip='10.0.0.4/24')
        
        # Add custom DNS resolver (for later parts)
        dns = self.addHost('dns', ip='10.0.0.5/24')
        
        # Add a NAT node for internet access
        nat = self.addNode('nat0', cls=NAT, ip='10.0.0.254/24', inNamespace=False)
        
        # Links for hosts
        self.addLink(h1, s1, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h2, s2, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h3, s3, cls=TCLink, bw=100, delay='2ms')
        self.addLink(h4, s4, cls=TCLink, bw=100, delay='2ms')
        
        # Links between switches and the custom dns resolver
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='5ms')
        self.addLink(s2, s3, cls=TCLink, bw=100, delay='8ms')
        self.addLink(s3, s4, cls=TCLink, bw=100, delay='10ms')
        self.addLink(dns, s2, cls=TCLink, bw=100, delay='1ms')
        
        # Connect the NAT node to the central switch
        self.addLink(s2, nat)

def run():
    topo = AssignmentTopo()
    net = Mininet(topo=topo, controller=Controller, link=TCLink, switch=OVSSwitch, autoSetMacs=True)
    net.start()
    
    # Add a default route for each host to reach the internet via NAT
    for host in ['h1', 'h2', 'h3', 'h4', 'dns']:
        h = net.get(host)
        # Set the default route to go through the NAT gateway
        h.cmd(f'ip route add default via 10.0.0.254')
        
        # --- FIX 2: Force host to use a public DNS server ---
        # This overwrites the host's DNS config to use Google's DNS
        h.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
        
    print("\nNetwork started with internet connectivity.\n")

    # --- Automatically Run Part B DNS Resolution Script ---
    print("--- Starting Part B: DNS resolution test on h1... ---")
    h1 = net.get('h1')
    
    # Command to run on h1. Assumes all files are in the same directory.
    # It will use the 100 domains from your text file.
    command = 'python3 part_b_resolver.py domains_h1_unique.txt h1_default_results.csv'
    command2 = 'python3 part_b_resolver.py domains_h2_unique.txt h2_default_results.csv'
    command3 = 'python3 part_b_resolver.py domains_h3_unique.txt h3_default_results.csv'
    command4 = 'python3 part_b_resolver.py domains_h4_unique.txt h4_default_results.csv' 
    # Execute the command on h1 and print its output
    result1 = h1.cmd(command)
    result2 = h1.cmd(command2)
    result3 = h1.cmd(command3)
    result4 = h1.cmd(command4)
    print(result1)
    print("--- DNS resolution test on h1 complete. ---")
    print(f"Results have been saved to 'h1_default_results.csv' on the host.")
    print(result2)
    print("--- DNS resolution test on h2 complete. ---")
    print(f"Results have been saved to 'h2_default_results.csv' on the host.")
    print(result3)
    print("--- DNS resolution test on h3 complete. ---")
    print(f"Results have been saved to 'h3_default_results.csv' on the host.")
    print(result4)
    print("--- DNS resolution test on h4 complete. ---")
    print(f"Results have been saved to 'h4_default_results.csv' on the host.")
    print("\nStarting Mininet CLI...\n")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()



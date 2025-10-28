# B. DNS Traffic Analysis From Packet Files

## Files in This Repository

- **topo_b.py** – Defines a custom Mininet topology, setting up hosts, switches, and links as per the assignment.  
- **part_b_resolver.py** – Responsible for handling DNS resolution simulation and managing the network interactions between hosts.  
- **PCAP_*.pcap** – Wireshark capture files generated from traffic between Mininet hosts.  
- **domains_\*\.txt / domains_*_unique.txt** – Processed DNS query name lists extracted from PCAP files.

---

### 1. Launch the Mininet Topology

Run the custom topology file inside your Mininet environment:

```bash
sudo python3 topo_b.py
```

This will:
- Create the specified hosts (e.g., `h1`, `h2`, etc.)
- Establish links between switches and hosts.
- Start a controller and network simulation.

### 2. Run the Resolver Script

Once the topology is running, execute the resolver logic in another terminal:

```bash
sudo python3 part_b_resolver.py
```

This script performs DNS query simulations and records traffic data that can later be analyzed.

---

## Generating Domain Name Text Files from PCAP

After running the simulation, you will have `.pcap` files such as `PCAP_1_H1.pcap`.  
To extract unique DNS query names from them, use the following commands:

```bash
tshark -r PCAP_1_H1.pcap -Y "dns && dns.qry.name"        -T fields -e dns.qry.name > domains_h1.txt

awk '{gsub(/\.$/,""); print}' domains_h1.txt | awk '!seen[$0]++'        > domains_h1_unique.txt
```

### Explanation:
- **tshark**: Reads the `.pcap` file and extracts all DNS query names (`dns.qry.name` field).  
- **awk** (first command): Removes trailing dots from domain names.  
- **awk** (second command): Removes duplicates to create a clean, unique list of domain names.  
- The final output is saved in `domains_h1_unique.txt`.

---

## Files and what they does

1. **Mininet Topology Creation** – The topology script defines hosts and switches, assigns IPs, and establishes connectivity.  
2. **Traffic Generation** – The resolver script simulates DNS queries or other network requests between hosts.  
3. **Packet Capture** – The simulation records traffic into `.pcap` files.  
4. **Traffic Analysis** – Using `tshark`, we parse the PCAP files to extract DNS query names and analyze host behavior.

---

## Example Directory Structure

```
.
├── topo_b.py
├── part_b_resolver.py
├── PCAP_*_H*.pcap (couldn't be included because of large size)
├── domains_h*.txt
├── domains_h*_unique.txt
└── README.md
```

---

## Notes

- Always run Mininet scripts with `sudo`.  
- Ensure tshark can access `.pcap` files in the correct directory.  
- You can modify the topology in `topo_b.py` for testing different network configurations.


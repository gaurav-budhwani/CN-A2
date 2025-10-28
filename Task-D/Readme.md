# D. Custom DNS Resolver Experiment using Mininet

The resolver captures detailed DNS resolution steps, including timestamps, query stages (Root, TLD, Authoritative), response/referral behavior, and latency. The setup was validated using provided PCAP traces, and DNS resolution metrics such as:
- **Total DNS servers visited**, and  
- **Total DNS latency per query**  

were visualized for the **first 10 queried domains** for PCAP_1_H1.pcap.

---

## Structure

```
📂 Custom-DNS-Resolver/
│
├── net_topo.py               # Mininet topology script (defines hosts, links, and DNS server node)
├── cr.py                     # Custom DNS resolver script (handles query resolution and caching)
├── bench.py                  # Benchmarking script to run DNS queries from hosts
├── plot.py                   # Python plotting script for analysis and visualization
│
├── plot_servers_visited.png  # Graph: Number of DNS servers visited for first 10 domains
├── plot_latency.png          # Graph: DNS latency per domain for first 10 domains
│
└── README.md                 # Project documentation (this file)
```

---
Repeat DNS resolution for the given PCAP files using your custom DNS resolver (10.0.0.5) and compare with the default system resolver.


## Workflow

### 1. **Start the Custom DNS Resolver**
On the DNS resolver node:
```bash
sudo python3 cr.py
```
This resolver listens for DNS queries and performs resolution either from cache or via iterative lookups.

### 2. **Benchmark DNS Resolution**
From client hosts (e.g., H1):
```bash
sudo python3 bench.py
```
This triggers DNS queries to the custom resolver and logs latency data.

---

## Generating Input Data from PCAPs

Used **TShark** to extract DNS query and response data from `.pcap` files into `.txt` format for processing:

```bash
tshark -r PCAP_1_H1.pcap -Y "dns && dns.flags.response == 1" -T fields -e frame.time -e dns.qry.name -e dns.a -e dns.flags.rcode -e dns.retransmission > dns_log_PCAP1.txt
```

> Repeat for other PCAPs if multiple hosts or captures are available.

These `.txt` logs serve as inputs for `plot.py` to generate comparative performance plots.

---

## Visualizations

Two visualizations were generated using `plot.py`:

### 1. DNS Servers Visited per Domain
<img width="1500" height="700" alt="plot_servers_visited" src="https://github.com/user-attachments/assets/1f03e4e6-d08d-468f-8645-c31232188514" />

- Each bar represents how many DNS servers were contacted for resolving a domain.
- For the first 10 URLs, all visited **1 server** (indicating cache hits or short resolution chains).

### 2. DNS Latency per Domain
<img width="1500" height="700" alt="plot_latency" src="https://github.com/user-attachments/assets/2590d11e-5751-465a-b8d8-53040723261c" />
- Displays the total DNS resolution latency (ms) per domain.
- Some domains show significantly higher latency due to:
  - Cache misses
  - Multi-step resolution (Root → TLD → Authoritative)
  - Remote authoritative servers or network congestion

---

## Dependencies

Ensure you have the following installed:

```bash
sudo apt update
sudo apt install tshark python3 python3-pip mininet
pip3 install matplotlib pandas
```

---

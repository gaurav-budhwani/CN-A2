# C. Custom DNS Resolver Configuration in Mininet

## Files in This Repository

- **topo_cr.py** – Defines the custom Mininet topology (hosts, switches, and links).  
- **cr.py** – Implements the **custom DNS resolver** that handles DNS requests from the Mininet hosts and responds accordingly.

## Instructions 
### Step 1: Launch the Custom Topology

Run the topology file inside Mininet:

```bash
sudo python3 topo_cr.py
```

This script will:
- Create multiple hosts (e.g., `h1`, `h2`, etc.).  
- Connect them via a switch and controller.  
- Assign IP addresses to each host.  

Once launched, you will get the Mininet CLI prompt.

---

### Step 2: Start the Custom Resolver

In another terminal window, run the custom resolver script:

```bash
sudo python3 cr.py
```

This script starts a DNS resolver that listens on **UDP port 53** and handles DNS queries manually.

---

## Internet Connectivity
The new DNS is connected to the internet, and this can be checked using ```nslookup``` or ```dig``` command inside the mininet CLI.
For example:
```
mininet> h1 nslookup google.com
mininet> h2 nslookup amazon.com
mininet> h3 nslookup amazon.in
mininet> h4 nslookup teams.microsoft.com
```

<img width="1600" height="1001" alt="image" src="https://github.com/user-attachments/assets/388a63e4-29dd-4a5f-a051-e4d0d5324184" />

## How It Works

1. **Custom Resolver (`cr.py`)** – Implements a simple DNS resolver that listens for DNS requests and sends back responses.  
2. **Topology Setup (`topo_cr.py`)** – Builds the Mininet environment with multiple hosts and a switch.  
3. **DNS Redirection** – Each host’s `/etc/resolv.conf` is modified to point to the custom resolver’s IP.  
4. **Testing** – DNS queries from hosts are captured and resolved by the custom DNS service.

---


## Note

- Always execute Mininet scripts using `sudo`.  
- The DNS resolver must run before performing `nslookup` from any host.  
- Make sure UDP port 53 is not blocked or used by another process.  

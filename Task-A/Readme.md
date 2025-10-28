## Task A

1. Defines an `AssignmentTopo` class (subclass of `mininet.topo.Topo`) with a `build()` method that:
   - Adds 4 switches: `s1`, `s2`, `s3`, `s4`.
   - Adds 4 hosts with fixed IPs:
     - `h1` — `10.0.0.1/24`
     - `h2` — `10.0.0.2/24`
     - `h3` — `10.0.0.3/24`
     - `h4` — `10.0.0.4/24`
   - Adds a host `dns` created with IP `10.0.0.5/24`.
   - Connects each host to its corresponding switch using `TCLink` with `bw=100` and `delay='2ms'`.
   - Connects switches in a chain:
     - `s1 <-> s2` with `bw=100` and `delay='5ms'`
     - `s2 <-> s3` with `bw=100` and `delay='8ms'`
     - `s3 <-> s4` with `bw=100` and `delay='10ms'`
   - Connects `dns` to `s2` with `bw=100` and `delay='1ms'`.

2. The `run()` function:
   - Instantiates the topology and a `Mininet` object: `Mininet(topo=topo, controller=Controller, link=TCLink, switch=OVSSwitch, autoSetMacs=True)`.
   - Starts the network (`net.start()`).
   - Prints status, runs `net.pingAll()` so Mininet pings all hosts once, then launches the Mininet CLI (`CLI(net)`).
   - On exit from the CLI it stops the network (`net.stop()`).

---

## Important Notes

- **Controller:** the script uses Mininet's default `Controller`.

- **Bandwidth/delay values:** `TCLink` parameters are honored only if `tc` (traffic control) is available in the host system. On a typical Linux VM they are available. If you get errors, ensure `iproute2`/`tc` are installed.

---

## Dependencies

- **OS:** A Linux environment is recommended (Ubuntu 18.04/20.04/22.04 commonly used for Mininet). Running Mininet inside macOS is possible only inside a Linux VM.
- **Python:** Python 3 (the script starts with `#!/usr/bin/env python3`)
- **Mininet:** the topology is built on Mininet (includes `mininet.node`, `mininet.net`, `mininet.cli`, `mininet.topo`, etc.)
- `tc`/`iproute2` utilities (for TCLink shaping) — usually included in modern Linux distributions.

---

## Install Mininet (Ubuntu / Debian)

A quick install (recommended on a fresh Ubuntu VM):

```bash
# system update & dependencies
sudo apt-get update
sudo apt-get install -y git python3-pip

# recommended: install mininet via apt (easiest)
sudo apt-get install -y mininet

# or (if you want latest from source)
# git clone https://github.com/mininet/mininet
# cd mininet
# ./utils/install.sh -a    # -a installs all dependencies (may take a while)
```

After installing, verify with:
```bash
sudo mn --test pingall
```
You should see a working Mininet and successful pings.

---

## How to run `topo.py`

1. Open a terminal on the machine where Mininet is installed (usually an Ubuntu VM).
2. Make sure the script is executable (optional):
   ```bash
   chmod +x topo.py
   ```
3. Run it with root privileges:
   ```bash
   sudo python3 topo.py
   ```
   or
   ```bash
   sudo ./topo.py
   ```

**Expected behaviour:**
- Mininet starts, creates the topology and the default controller.
- The script will run `net.pingAll()` and you will see ping success/failure summary.
- The Mininet CLI prompt appears: `mininet>`. You can now run interactive commands.

---

## Useful Mininet CLI commands (once inside CLI)

- `nodes` — list nodes (hosts, switches, controllers).
- `net` — show the network graph (node connections).
- `dump` — show interfaces and IPs for every node.
- `h1 ifconfig` — run `ifconfig` on host `h1`.
- `h1 ping h2` — ping from `h1` to `h2`.
- `h1 ip route` — show routing table of `h1`.
- `h1 tcpdump -i h1-eth0` — capture packets on h1 interface (requires tcpdump installed).
- `exit` or press `Ctrl+D` — leave CLI and stop the network.

---

## Example checks / tests to run

From CLI:
```bash
mininet> h1 ping -c 3 h2
mininet> h1 ping -c 3 dns
mininet> dump
```

Because `TCLink` is used with `bw` and `delay` arguments, you should observe:
- Higher latency on paths that traverse `s3`->`s4` (10ms) vs `s1`->`s2` (5ms).
- Round-trip delays reflect link delays cumulatively along paths between hosts.

---

## How the topology maps logically

```
h1(10.0.0.1) --- s1 --- s2 --- s3 --- s4 --- h4(10.0.0.4)
                     |
                   dns(10.0.0.5)
h2(10.0.0.2) --- s2
h3(10.0.0.3) --- s3
```

- Each `hX` is connected to its own switch (`h1`→`s1`, `h2`→`s2`, `h3`→`s3`, `h4`→`s4`).
- Switches are wired in series: `s1 - s2 - s3 - s4`.
- `dns` is attached to `s2`.

---

## Extending / modifying the script

- To change link bandwidth/delay, edit the `self.addLink(...)` calls and adjust `bw=` and `delay=` values.
- To attach additional hosts, add `h5 = self.addHost('h5', ip='10.0.0.6/24')` and `self.addLink(h5, s3, cls=TCLink, bw=100, delay='2ms')`.
- To use a remote controller:
  ```python
  from mininet.node import RemoteController
  net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633), ...)
  ```
  or instantiate `RemoteController('c0', ip='CONTROLLER_IP')` as needed.
- To set static routes or run services on `dns`, use `dns.cmd('...')` from `run()` or drop into CLI and run commands interactively.

---

## Troubleshooting

- **Permission errors / OVS errors:** always run Mininet scripts as `sudo`.
- **TCLink shaping not applied / `tc` missing:** install `iproute2` (`sudo apt-get install iproute2`) and retry.
- **If `net.pingAll()` fails:** check IP addresses (`dump`) and interface states (`ifconfig`) in the CLI.
- **If script fails to import Mininet modules:** ensure Mininet is installed and your `PYTHONPATH` includes Mininet (install via apt or from source).

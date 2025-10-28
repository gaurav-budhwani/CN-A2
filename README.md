# CN-A2
Assignment 2 for the course Computer Networks (CS331)
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

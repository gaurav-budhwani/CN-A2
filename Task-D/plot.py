#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys

LOG_FILE = "/tmp/resolver.log"
NUM_QUERIES = 10

def extract_query_info(log_path):
    """Turn resolver/forwarder logfile text into a structured table for plotting."""
    print(f"Loading log file: {log_path}")
    queries = []
    curr = {}
    try:
        with open(log_path, "r") as file:
            for line in file:
                # looking for lines mentioning the queried domain name
                domain = re.search(r'b\. Domain Name: (.*)', line)
                if domain:
                    if curr:
                        queries.append(curr)
                    curr = {'domain': domain.group(1).strip()}
                # pull out the resolution time (latency)
                latency = re.search(r'h\. Overall Time: ([\d.]+) ms', line)
                if latency and curr:
                    curr['latency_ms'] = float(latency.group(1))
                    curr['servers_visited'] = 1
        # adding the last found query
        if curr:
            queries.append(curr)
    except FileNotFoundError:
        print(f"Log file not found at {log_path}. Did you run the DNS experiment?")
        return None
    if not queries:
        print("No queries found in log. Check your DNS experiment and log formatting.")
        return None
    return pd.DataFrame(queries)

def make_plots():
    """parsing the DNS logs and draw/save the requested plots."""
    df = extract_query_info(LOG_FILE)
    if df is None:
        sys.exit(1)
    subset = df.head(NUM_QUERIES)
    print(f"Preparing plots for {len(subset)} queries...")
    plt.figure(figsize=(12, 6))
    plt.bar(subset['domain'], subset['latency_ms'], color='darkcyan')
    plt.title(f'DNS Resolution Latency (First {len(subset)} Queries)')
    plt.xlabel('Domain Name')
    plt.ylabel('Latency (ms)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('plot_latency.png')
    print("Latency plot saved as 'plot_latency.png'")
    plt.close()
    # DNS servers hit for each query (always 1 in this setup)
    plt.figure(figsize=(12, 6))
    plt.bar(subset['domain'], subset['servers_visited'], color='coral')
    plt.title(f'DNS Servers Contacted (First {len(subset)} Queries)')
    plt.xlabel('Domain Name')
    plt.ylabel('Servers Visited')
    plt.yticks(range(0, int(subset['servers_visited'].max()) + 2))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('plot_servers_visited.png')
    print("Servers visited plot saved as 'plot_servers_visited.png'")
    plt.close()

if __name__ == "__main__":
    make_plots()

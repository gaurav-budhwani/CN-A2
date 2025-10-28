#!/usr/bin/python3
"""
benchmark file which measures the dns resolution performance (latency, throughput) by querying
each domain using the 'dig' utility.
"""
import sys
import subprocess
import time
import re
from scapy.all import rdpcap, DNS, DNSQR

# directly use the pcap file to extract the domains, was taking too much time in macOS due to swap memory caching
# so we used tshark instead and moved on with the bench.py script to further evaluate the metrics needed.
def scan_pcap_for_domains(capture_filename):
    """
    Scans a packet capture file to extract all unique domain names from DNS queries.
    """
    unique_domains = set()
    print(f"--> Analyzing '{capture_filename}' for DNS queries...")
    try:
        packets = rdpcap(capture_filename)
        # iterate through each packet to find DNS queries
        for packet in packets:
            # A DNS query has a DNS layer, a DNS Question Record (DNSQR), and the 'qr' flag set to 0.
            if packet.haslayer(DNS) and packet.haslayer(DNSQR) and packet[DNS].qr == 0:
                try:
                    # The qname is in bytes (e.g., b'google.com.') - decode and clean it up.
                    domain = packet[DNSQR].qname.decode('utf-8').rstrip('.')
                    if domain:
                        unique_domains.add(domain)
                except UnicodeDecodeError:
                    # Silently ignore domains that can't be decoded properly.
                    pass
                    
    except FileNotFoundError:
        print(f"[ERROR] The file '{capture_filename}' was not found.")
        return []
    except Exception as e:
        print(f"[ERROR] A problem occurred while reading the PCAP file: {e}")
        return []

    if not unique_domains:
        print("--> No valid DNS queries were found in the capture file.")
        
    return list(unique_domains)

def run_performance_test(domain_list):
    """
    Performs DNS lookups for a list of domains and measures performance.
    """
    if not domain_list:
        print("[Warning] The list of domains to test is empty. Aborting benchmark.")
        return

    query_times = []
    successful_queries = 0
    failed_queries = 0
    benchmark_start_time = time.time()

    print(f"--> Starting benchmark for {len(domain_list)} unique domains...")

    for domain in domain_list:
        try:
            # we run 'dig' twice: once to check for a valid response,
            # and a second time with '+stats' to parse the query time.
            check_command = ['dig', '+short', '+time=2', domain]
            check_result = subprocess.run(check_command, capture_output=True, text=True, timeout=5)
            
            # A successful query returns a non-empty stdout and a zero return code.
            if check_result.returncode == 0 and check_result.stdout.strip():
                stats_command = ['dig', '+stats', '+time=2', domain]
                stats_result = subprocess.run(stats_command, capture_output=True, text=True, timeout=5)
                
                # using regex to find the 'Query time' line in the output.
                time_match = re.search(r'Query time: (\d+) msec', stats_result.stdout)
                if time_match:
                    latency_ms = int(time_match.group(1))
                    query_times.append(latency_ms)
                    successful_queries += 1
                else:
                    failed_queries += 1 # Succeeded but couldn't parse time.
            else:
                failed_queries += 1
                
        except subprocess.TimeoutExpired:
            failed_queries += 1
        except Exception:
            failed_queries += 1

    benchmark_end_time = time.time()
    
    total_duration = benchmark_end_time - benchmark_start_time
    average_latency = sum(query_times) / len(query_times) if query_times else 0
    queries_per_second = len(domain_list) / total_duration if total_duration > 0 else 0

    print("\n--- Performance Benchmark Summary ---")
    print(f"  Total Domains Tested: {len(domain_list)}")
    print(f"  Successful Lookups:   {successful_queries}")
    print(f"  Failed Lookups:       {failed_queries}")
    print(f"  Average Query Time:   {average_latency:.2f} ms")
    print(f"  Overall Throughput:   {queries_per_second:.2f} queries/sec")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <path_to_pcap_file>")
        sys.exit(1)
        
    pcap_filename = sys.argv[1]
    domains_to_test = scan_pcap_for_domains(pcap_filename)
    
    if domains_to_test:
        run_performance_test(domains_to_test)
    else:
        print("--> Benchmark finished with no domains to test.")

import sys
import subprocess
import time
import re
# extarct the pcap files to txt file and then use it as an input
def read_domains_from_txt(txt_filename):
    domains = []
    print(f"--> Reading domain names from '{txt_filename}'...")
    try:
        with open(txt_filename, 'r') as f:
            for line in f:
                # cleaning up the line by removing whitespace and newlines
                domain = line.strip()
                if domain:  # making sure the line is not empty
                    domains.append(domain)
    except FileNotFoundError:
        print(f"[ERROR] The file '{txt_filename}' was not found.")
        return []
    except Exception as e:
        print(f"[ERROR] A problem occurred while reading the text file: {e}")
        return []
    if not domains:
        print("--> No domains were found in the file.")
        
    return domains

def run_performance_test(domain_list):
    """
    DNS lookups for a list of domains and measures performance.
    """
    if not domain_list:
        print("[Warning] The list of domains to test is empty. Aborting benchmark.")
        return
    query_times = []
    successful_queries = 0
    failed_queries = 0
    benchmark_start_time = time.time()

    print(f"--> Starting benchmark for {len(domain_list)} domains...")

    for domain in domain_list:
        try:
            # we run 'dig' twice: once to check for a valid response,
            # and a second time with '+stats' to parse the query time.
            check_command = ['dig', '+short', '+time=2', domain]
            check_result = subprocess.run(check_command, capture_output=True, text=True, timeout=5)
            # successful query returns a non-empty stdout and a zero return code.
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
        # Updated usage message to reflect the change to .txt file input
        print(f"Usage: python3 {sys.argv[0]} <path_to_domains_file.txt>")
        sys.exit(1)
        
    txt_filename = sys.argv[1]
    # Call the new function to read from the text file
    domains_to_test = read_domains_from_txt(txt_filename)
    
    if domains_to_test:
        run_performance_test(domains_to_test)
    else:
        print("--> Benchmark finished with no domains to test.")

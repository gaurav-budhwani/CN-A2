#!/usr/bin/env python3
import sys, socket, time, csv

def resolve(domain):
    start = time.perf_counter()
    try:
        # Use socket.getaddrinfo() to use the default system resolver
        res = socket.getaddrinfo(domain, None)
        elapsed = (time.perf_counter() - start) * 1000.0 # Convert to ms
        ips = sorted({r[4][0] for r in res if r and r[4]})
        return True, elapsed, ips
    except Exception:
        # On failure, still record the time taken
        elapsed = (time.perf_counter() - start) * 1000.0 # Convert to ms
        return False, elapsed, []

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: part_b_resolver.py domain_list.txt out.csv [--pause 0.01]")
        sys.exit(1)
        
    infile = sys.argv[1]
    outfile = sys.argv[2]
    pause = 0.0
    
    if '--pause' in sys.argv:
        pause = float(sys.argv[sys.argv.index('--pause')+1])

    print(f"Starting DNS resolution for domains in '{infile}'...")
    
    with open(infile) as inf, open(outfile, 'w', newline='') as outf:
        w = csv.writer(outf)
        w.writerow(['timestamp','domain','success','rtt_ms','ips'])
        
        count = 0
        successes = 0
        total_latency_ms = 0.0
        t0 = time.perf_counter()

        for line in inf:
            dom = line.strip()
            if not dom:
                continue
            
            ok, rtt, ips = resolve(dom)
            w.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"), dom, int(ok), f"{rtt:.3f}", ";".join(ips)])
            
            if ok:
                successes += 1
                total_latency_ms += rtt
                
            count += 1
            if pause:
                time.sleep(pause)
                
        t_total_s = time.perf_counter() - t0

    # --- Calculate and Print Final Statistics ---
    
    failed_resolutions = count - successes
    # Only calculate average latency for successful queries
    avg_latency_ms = total_latency_ms / successes if successes > 0 else 0.0
    # Throughput is successful queries per second
    avg_throughput_qps = successes / t_total_s if t_total_s > 0 else 0.0

    print(f"Total Queries:            {count}")
    print(f"Successful Resolutions:   {successes}")
    print(f"Failed Resolutions:       {failed_resolutions}")
    print(f"Total Time Taken:         {t_total_s:.2f} seconds")
    print(f"Average Lookup Latency:   {avg_latency_ms:.2f} ms")
    print(f"Average Throughput:       {avg_throughput_qps:.2f} queries/sec")

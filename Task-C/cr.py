#!/usr/bin/python3

import socket
import socketserver
import time
import datetime

# Chosen upstream DNS to relay queries
UPSTREAM_DNS_SERVER = "8.8.8.8"
UPSTREAM_DNS_PORT = 53

DNS_CACHE = {}

CACHE_ENABLED = False

class ForwardingDNSHandler(socketserver.BaseRequestHandler):
    """
    processes incoming DNS requests.
    server provides proxy-like or forwarding capability for DNS.
    """
    def extract_domain_name(self, packet):
        """extarcts packets"""
        try:
            # DNS header is 12 bytes long
            # The query name starts after the header
            header = packet[:12]
            question = packet[12:]
            # Find the end of the QNAME field
            qname_termination = question.find(b'\x00')
            raw_qname = question[:qname_termination]
            # Convert DNS QNAME to dot-separated domain
            domain_parts = []
            idx = 0
            while idx < len(raw_qname):
                seg_len = raw_qname[idx]
                idx += 1
                domain_parts.append(raw_qname[idx: idx + seg_len].decode('utf-8'))
                idx += seg_len
            domain_name = ".".join(domain_parts)
            return domain_name
        except Exception as err:
            print(f"[Forwarder] Failed to parse domain: {err}")
            return None

    def handle(self):
        payload, client_socket = self.request
        requester_ip = self.client_address
        log_time = datetime.datetime.now().isoformat()
        requested_domain = self.extract_domain_name(payload)

        if not requested_domain:
            return  # skip malformed queries

        print("DNS Query Log (Alternate)")
        print(f"a. Timestamp: {log_time}")
        print(f"b. Domain Name: {requested_domain}")

        cache_state = "MISS"

        if cache_state != "HIT":
            print("i. Cache State: NOT_FOUND")
        #print("c. Resolution Strategy: Forward (Non-recursive)")
        # forward the query to the real DNS server
        relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        relay_socket.settimeout(2.0)

        try:
            send_time = time.time()
            relay_socket.sendto(payload, (UPSTREAM_DNS_SERVER, UPSTREAM_DNS_PORT))
            print(f"d. Upstream DNS Contacted: {UPSTREAM_DNS_SERVER}")
            print("e. Action: Relayed Upstream")
            response, _ = relay_socket.recvfrom(512)
            recv_time = time.time()
            latency = (recv_time - send_time) * 1000
            print(f"f. Upstream Response: Received")
            print(f"g. Upstream RTT: {latency:.2f} ms")
            print(f"h. Overall Time: {latency:.2f} ms")
            client_socket.sendto(response, requester_ip)
        except socket.timeout:
            print("f. Upstream Response: Timeout")
        except Exception as err:
            print(f"[Forwarder] Error during forwarding: {err}")
        finally:
            relay_socket.close()
            print("------------------------\n")

if __name__ == "__main__":
    LISTEN_IP, LISTEN_PORT = "10.0.0.5", 53
    print(f"DNS Forwarder active at {LISTEN_IP}:{LISTEN_PORT}...")
    try:
        with socketserver.UDPServer((LISTEN_IP, LISTEN_PORT), ForwardingDNSHandler) as server:
            server.serve_forever()
    except Exception as err:
        print(f"!! [Forwarder] LAUNCH FAILURE: {err} !!")
        print("!! You may need 'sudo' to execute this script !!")

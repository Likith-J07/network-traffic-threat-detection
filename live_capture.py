from scapy.all import sniff
from scapy.layers.inet import TCP, UDP, ICMP
import requests

def process_packet(packet):
    if packet.haslayer('IP'):
        # Get protocol as string
        if packet.haslayer(TCP):
            protocol = "TCP"
        elif packet.haslayer(UDP):
            protocol = "UDP"
        elif packet.haslayer(ICMP):
            protocol = "ICMP"
        else:
            protocol = "Other"

        packet_size = len(packet)
        flow_duration = 0.01  # Placeholder; improve if needed
        flags = '-'  # Placeholder, can be refined
        src_ip = packet['IP'].src
        dst_ip = packet['IP'].dst

        data = {
            "Protocol": protocol,
            "Packet_Size": packet_size,
            "Flow_Duration": flow_duration,
            "Flags": flags,
            "Src_IP": src_ip,
            "Dst_IP": dst_ip
        }

        try:
            # Make POST request with API key header (replace with your key)
            headers = {"X-API-KEY": "my_secret_api_key"}
            response = requests.post("http://localhost:5000/predict", json=data, headers=headers)
            print("Sent data:", data)
            print("Response:", response.text)
        except Exception as e:
            print(f"Error sending data: {e}")

sniff(prn=process_packet, count=50)  # Capture 50 packets; remove count for continuous capture

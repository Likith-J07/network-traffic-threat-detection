import pandas as pd
import time
import requests

df = pd.read_csv("synthetic_network_traffic.csv")

print("🔄 Starting traffic simulation...\n")

for i, row in df.iterrows():
    data = {
        'Protocol': row['Protocol'],
        'Packet_Size': row['Packet_Size'],
        'Flow_Duration': row['Flow_Duration'],
        'Flags': row['Flags'],
        'Src_IP': row['Src_IP'],
        'Dst_IP': row['Dst_IP']
    }

    try:
        response = requests.post("http://localhost:5000/predict", json=data)
        resp_json = response.json()
        print(f"[{i+1}] Sent packet: {data} → Prediction: {resp_json['prediction']}, Src_IP: {resp_json['Src_IP']}, Dst_IP: {resp_json['Dst_IP']}")
    except Exception as e:
        print(f"❌ Failed to send data: {e}")

    time.sleep(1)

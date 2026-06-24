import socket
import struct
import threading
from collections import deque

UDP_IP = "127.0.0.1"
UDP_PORT = 6969

gas_history = deque([0.0] * 240, maxlen=240)
brake_history = deque([0.0] * 240, maxlen=240)
steer_history = deque([0.0] * 240, maxlen=240)

def harvest_telemetry():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((UDP_IP, UDP_PORT))
        print(f"Listening for data on port {UDP_PORT}...")
        

        while True:
            data, _ = s.recvfrom(1024)
            if len(data) < 320:
                continue
            try:    
                    is_race_on = struct.unpack('<i', data[0:4])[0]
                    
                    if not is_race_on:
                        continue
                    
                    gas = struct.unpack('<B', data[315:316])[0] / 255.0
                    brake = struct.unpack('<B', data[316:317])[0] / 255.0
                    steering = struct.unpack('<b', data[320:321])[0] / 127.0
                    
                    gas_history.append(gas)
                    brake_history.append(brake)
                    steer_history.append(steering)
            except Exception as e:
                print(f"Bad packet: {e}")
                
                
threading.Thread(target=harvest_telemetry, daemon=True).start()


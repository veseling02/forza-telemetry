import socket
import struct
import threading
import time
from collections import deque

UDP_IP = "0.0.0.0"
UDP_PORT = 6969

HISTORY_LEN = 240 # 4 seconds at Forza's 60 packets/sec

gas_history = deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)
brake_history = deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)
steer_history = deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)
speed_history = deque([0.0] * HISTORY_LEN, maxlen=HISTORY_LEN)
latest = {"rpm": 0.0, "rpm_frac": 0.0, "speed": 0.0}

def _harvest(sock):
    with sock:
        print(f"Listening for data on port {UDP_PORT}...")
        

        while True:
            data, _ = sock.recvfrom(1024)
            if len(data) < 321:
                continue
            try:    
                is_race_on = struct.unpack('<i', data[0:4])[0]
                
                if not is_race_on:
                    continue
                
                gas = struct.unpack('<B', data[315:316])[0] / 255.0
                brake = struct.unpack('<B', data[316:317])[0] / 255.0
                steering = max(-1, struct.unpack('<b', data[320:321])[0] / 127.0)
                speed = struct.unpack('<f', data[256:260])[0] * 3.6
                rpm = struct.unpack('<f', data[16:20])[0]
                max_rpm = struct.unpack('<f', data[8:12])[0]
                
                latest['rpm'] = rpm
                latest['rpm_frac'] = rpm / max_rpm if max_rpm > 0 else 0.0
                latest['speed'] = speed
                gas_history.append(gas)
                brake_history.append(brake)
                steer_history.append(steering)
                speed_history.append(speed)
                
            except Exception as e:
                print(f"Bad packet: {e}")
                
                
def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    threading.Thread(target=_harvest, args=(sock,), daemon=True).start()

if __name__ == "__main__":
    print("--- RUNNING HARVESTER DIAGNOSTIC ---")
    start()
    while True:
        print(f"Gas: {gas_history[-1]:.2f} | Speed: {speed_history[-1]:.1f} km/h")
        time.sleep(0.2)
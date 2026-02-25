import socket
import os
from a51 import A5_dec, A5_enc
from comp128.comp128v23 import Comp128v23

HOST = "127.0.0.1"
PORT = 5000
MAX_BYTES = 32

IMSI = b"000112233333333"
Ki = bytearray(bytes.fromhex("00112233445566778899AABBCCDDEEFF"))

def send_IMSI(s):
    s.sendall(IMSI)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    #=== Send IMSI (International Mobile Subscriber Identity) ===
    send_IMSI(s)
    print(f"[+] Sent IMSI")

    #=== Receive challenge and calculate the SRES response and temporary key ===

    chall = s.recv(1024)
    print(f"[+] Received challenge: {chall}")

    v3_sres, v3_kc = Comp128v23().comp128v3(Ki, chall)

    print(f"[+] Generated SRES: {v3_sres} and temporary key {v3_kc}")

    s.sendall(v3_sres)
    print(f"[+] Sent SRES: {v3_sres}")

    #=== Start of encrypted communication

    input_file = "file.txt"
    output_dir = "received_client"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "rb") as f:
        data = f.read()

    if len(data) > MAX_BYTES:
        raise ValueError(f"File too large: {len(data)} bytes (max {MAX_BYTES} bytes)")
    
    #send encrypted message
    c = A5_enc(data, v3_kc)

    s.sendall(c)


    c = s.recv(1024)
    print(c)
    print(A5_dec(c, v3_kc))





import socket
import secrets
import os
from a51 import A5_dec, A5_enc
from comp128.comp128v23 import Comp128v23

HOST = "127.0.0.1"
PORT = 5000
MAX_BYTES = 32


users = {
    b"000112233333333": bytes.fromhex("00112233445566778899AABBCCDDEEFF")
}

def generate_challenge():
    return secrets.token_bytes(16)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[+] Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()
        with conn:
            print(f"[+] Connected")

            #=== First message received: IMSI (International Mobile Subscriber Identity) ===

            imsi = conn.recv(1024)
            print(f"[+] Received IMSI: {imsi}")

            Ki = users[imsi]

            #TODO check for no match

            print(f"[+] Using Ki = {Ki}")

            #=== AuC generates the challenge and temp key using comp128 ===

            chall = generate_challenge()
            v3_sres, v3_kc = Comp128v23().comp128v3(Ki, chall)
            #TODO generate timsestamp

            print(f"[+] Generated challenge: {chall} -> SRES: {v3_sres} and temporary key {v3_kc}")

            #=== Send challenge to client ===

            conn.sendall(chall)
            print(f"[+] Sent challenge: {chall}")

            #=== Receive and verify response ===

            response_sres = conn.recv(1024)
            print(f"[+] Received response SRES: {response_sres}")

            if len(v3_sres) != len(response_sres):
                print(f"[+] Authentication failed")
                return
        
            for i in range(len(v3_sres)):
                if v3_sres[i] != response_sres[i]:
                    print(f"[+] Authentication failed")
                    return
            
            print(f"[+] Authentication successful, starting encrypted communication using temporary key {v3_kc}")

            #=== Auth done, start of encrypted comm ===

            enc_msg = conn.recv(1024)

            print(f"[+] Received message: {enc_msg}")

            #TODO check timestamp

            dec_msg = A5_dec(enc_msg, v3_kc)

            print(f"Message decrypted: {dec_msg}")

            conn.sendall(A5_enc(b"asdfasd", v3_kc))

                

start_server()
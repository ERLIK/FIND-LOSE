import socket
import tqdm
import os
import sys

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 

host = input('Enter server\'s ip address: ')
port = int(input('Enter server\'s port: '))

filename = '1GB.bin'

try:
    filesize = os.path.getsize(filename)
except FileNotFoundError:
    print('File not found!')
    sys.exit()

s = socket.socket()

print(f"[+] Connecting to {host}:{port}")

try:
    s.connect((host, port))
    print("[+] Connected.")
except (OSError,TimeoutError):
    print('Connection error, please check host address and physical connection and try again.')
    sys.exit()

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))
s.close()
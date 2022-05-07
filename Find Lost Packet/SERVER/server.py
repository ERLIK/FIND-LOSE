import socket
import tqdm
import os
import time

SERVER_HOST = input('Enter server\'s ip address: ')
SERVER_PORT = int(input('Enter server\'s port: '))

BUFFER_SIZE = 4096
SEPARATOR = '<SEPARATOR>'

s = socket.socket()
s.bind((SERVER_HOST,SERVER_PORT))

s.listen(5)
print(f'[-] Listening as {SERVER_HOST}:{SERVER_PORT}')

print('When a client is connected, the you should start SniffingTCP.py to displaying the packet stream.')
time.sleep(5)

client_socket, address = s.accept()
print(f'[-] {address} is connected.')

received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f'Receiving {filename}', unit='B', unit_scale= True, unit_divisor = 1024)

with open(filename, 'wb') as f:
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

client_socket.close()
s.close()
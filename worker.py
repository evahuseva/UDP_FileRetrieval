import os
import socket
import time
from os.path import exists

timeout = 3
bufferSize = 1024
msgFromWorker = "Worker 1 is connected and operating"
bytesToSend = str.encode(msgFromWorker, 'ascii')
serverAddressPort = ('172.25.0.3', 4900)

# Create a datagram socket
# Binding to address and ip
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind(('172.25.0.2', 4900))

print("UDP Worker is connected and operating.")

while True:
    time.sleep(1)
    bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print('Worker is doing something...')

    file_name = message.decode('utf-8')
    script_dir = os.path.dirname('cAssignment1')  # <-- absolute dir the script is in
    rel_path = file_name
    abs_file_path = os.path.join(script_dir, rel_path)

    if exists(file_name):
        f = open(file_name, 'rb')
        data = f.read(bufferSize)
        while data:
            if UDPWorkerSocket.sendto(data, serverAddressPort):
                data = f.read(bufferSize)
                time.sleep(1)
            print('Sent file to server.')
    else:
        UDPWorkerSocket.sendto(str.encode('NO_FILE'), serverAddressPort)
        print(f'No file {file_name} was found')


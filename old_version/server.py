import socket
import threading
from _thread import *


# Create a datagram socket
# Binding to address and ip
UDPServerClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerClientSocket.bind(('172.25.0.3', 4900))

UDPServerWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerWorkerSocket.bind(('172.25.0.3', 4916))

workerAddressPorts = [('172.25.0.2', 4916), ('172.25.0.5', 4916), ('172.25.0.6', 4916)]
clientAddressPort = ('172.25.0.4', 4900)
bufferSize = 1024

print('UDP server up and listening.')


def client_receiver():
    while True:
        client_buffer, client_address = UDPServerClientSocket.recvfrom(bufferSize)
        clientMsg = client_buffer.decode('utf-8')
        print(f'Client {client_address[0]} sent message <<{clientMsg}>>')
        if not client_buffer:
            break
        for workerAddressPort in workerAddressPorts:
            UDPServerWorkerSocket.sendto(client_buffer, workerAddressPort)  # sending file name to workers
            print(f'Client buffer sent to worker {workerAddressPort[0]}.')


def worker_sender():
    while True:
        worker_buffer = UDPServerWorkerSocket.recvfrom(bufferSize)[0]
        UDPServerClientSocket.sendto(worker_buffer, clientAddressPort)  # sending buffer data to client
        print(worker_buffer.decode('utf-8'))
        # print('Worker buffer sent to client.')
        while not worker_buffer:  # splitting the file to prevent buffer overflow
            worker_buffer = UDPServerWorkerSocket.recvfrom(bufferSize)[0]
            # print(f'Buffer received from worker {workerAddressPort[0]}.')
            UDPServerClientSocket.sendto(worker_buffer, clientAddressPort)
            # print('Worker buffer sent to client')
            print(worker_buffer.decode('utf-8'))


t1 = threading.Thread(target=client_receiver)
t1.start()

t2 = threading.Thread(target=worker_sender)
t2.start()

t1.join()
t2.join()

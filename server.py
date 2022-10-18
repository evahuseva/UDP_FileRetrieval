import socket
import time

timeout = 3
bufferSize = 1024
msgFromServer = "Server is connected and operating"
bytesToSend = str.encode(msgFromServer, 'ascii')
workerAddressPorts = [('172.25.0.2', 4900), ('172.25.0.5', 4900), ('172.25.0.6', 4900)]

# Create the datagram sockets for Client & Workers
# Binding datagrams to addresses and ip
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(('172.25.0.3', 4900))

# UDPServerWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerWorkerSocket.bind(('172.25.0.3', 4900))

print("UDP server up and listening")

while True:
    time.sleep(1)
    client_buffer = UDPServerSocket.recvfrom(bufferSize)[0]
    # with open(filename, mode="rb") as f:
    #    chunk = f.read(buffer_size)
    print('Server started its work and got some files from Worker.')

    clientMsg = "Message from Client:{}".format(client_buffer.decode('utf-8'))
    # workerMsg = "Message from Worker:{}".format(worker_buffer.decode('ascii'))
    # worker_buffer = UDPServerClientSocket.recvfrom(bufferWorkerSize)[0]

    for workerAddressPort in workerAddressPorts:
        UDPServerSocket.sendto(client_buffer, workerAddressPort)
        worker_buffer = UDPServerSocket.recvfrom(bufferSize)[0]
        print(worker_buffer.decode('utf-8'))
        while not worker_buffer:
            worker_buffer = UDPServerSocket.recvfrom(bufferSize)[0]
            print(worker_buffer.decode('utf-8'))



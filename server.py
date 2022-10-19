import socket
import time

bufferSize = 1024
workerAddressPorts = [('172.25.0.2', 4900), ('172.25.0.5', 4900), ('172.25.0.6', 4900)]
clientAddressPort = ('172.25.0.4', 4900)

# Create a datagram socket
# Binding to address and ip
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind(('172.25.0.3', 4900))

print('UDP server up and listening.')

while True:
    time.sleep(0.1)
    # getting file name from client
    client_buffer = UDPServerSocket.recvfrom(bufferSize)[0]
    # with open(filename, mode="rb") as f:
    #    chunk = f.read(buffer_size)
    print('Server started its work and received something from workers.')
    clientMsg = 'Message from client:{}'.format(client_buffer.decode('utf-8'))
    # workerMsg = "Message from Worker:{}".format(worker_buffer.decode('ascii'))
    for workerAddressPort in workerAddressPorts:
        UDPServerSocket.sendto(client_buffer, workerAddressPort)    # sending file name to worker
        worker_buffer = UDPServerSocket.recvfrom(bufferSize)[0]     # saving data from worker to buffer
        UDPServerSocket.sendto(worker_buffer, clientAddressPort)    # sending buffer data to client

        # print(worker_buffer.decode('utf-8'))
        # splitting the file to prevent buffer overflow:
        while not worker_buffer:
            worker_buffer = UDPServerSocket.recvfrom(bufferSize)[0]
            # print(worker_buffer.decode('utf-8'))
            UDPServerSocket.sendto(worker_buffer, clientAddressPort)
    print('Sent file to client.')

import socket
import time

msgFromClient = input('Name of the file to import: ')
print(msgFromClient)
bytesToSend = str.encode(msgFromClient, 'ascii')
serverAddressPort = ('172.25.0.3', 4900)
bufferSize = 1024

# Create a UDP socket at client side
# Send to server using created UDP socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

while True:
    time.sleep(1)
    server_buffer = UDPClientSocket.recvfrom(bufferSize)[0]
    msg = server_buffer.decode('utf-8')
    print('Client received something from the server.')
    print(msg)
    # new_file = open('client_writer.txt', 'w+')
    # data = new_file.write(bufferSize)
    if server_buffer:
        server_buffer = UDPClientSocket.recvfrom(bufferSize)[0]
        print(server_buffer.decode('utf-8'))
        if msg == 'NO_FILE':
            print('No such file in workers directory.')
        elif msg == 'END_OF_FßILE':
            print('Empty file.')
        else:
            print(msg)

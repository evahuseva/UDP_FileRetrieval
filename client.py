import socket

msgFromClient = input('name of the file to import: ')
print(msgFromClient)
bytesToSend = str.encode(msgFromClient, 'ascii')
serverAddressPort = ('172.25.0.3', 4900)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

while True:
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = msgFromServer[0].decode('utf-8')
    if msg == 'NO_FILE':
        print('no such file')

    elif msg == 'END_OF_FILE':
        print('empty file')

    else:
        print(msg)
    quit()



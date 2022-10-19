import socket
import sys
import time

msgFromClient = input('Name of the file to import: ')
print(msgFromClient)
bytesToSend = str.encode(msgFromClient, 'utf-8')
serverAddressPort = ('172.25.0.3', 4900)
bufferSize = 1024

# Create a UDP socket at client side
# Send to server using created UDP socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

while True:
    try:
        server_buffer = UDPClientSocket.recvfrom(bufferSize)[0]
        # breakpoint()
        if len(server_buffer) > 0:
            server_message = server_buffer.decode('utf-8')
            if server_message == 'NO_FILE':
                print('No such file in workers directory.')
                sys.exit()
            elif server_message == 'END_OF_FILE':
                print('Empty file.')
                sys.exit()
            else:
                f = open(msgFromClient, 'wb')
                f.write(server_buffer)
                f.close()
    except Exception as e:
        print(e)

import select
import socket
import sys
import time
import threading


msgFromClient = str(input('Name of the file to import: '))
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
bufferSize = 1024
serverAddressPort = ('172.25.0.3', 4900)


def sender():
    print(msgFromClient)
    bytesToSend = str.encode(msgFromClient, 'ascii')
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    return


def receiver():
    while True:
        time.sleep(0.1)
        try:
            while not select.select([UDPClientSocket], [], [], 0.1)[0]:
                pass
            server_buffer, server_address = UDPClientSocket.recvfrom(bufferSize)
            # breakpoint()
            server_message = server_buffer.decode('utf-8')
            print(f'Server {server_address[0]} sent message {server_message}')
            f = open(msgFromClient, 'wb')
            f.write(server_buffer)
            f.close()
            if len(server_buffer) > 0:
                server_message = server_buffer.decode('utf-8')
                if server_message == 'N':
                    print('No such file in workers directory.')
                    sys.exit()
                elif server_message == 'END_OF_FILE':
                    print('Empty file.')
                    sys.exit()
                else:
                    f = open(msgFromClient, 'wb')
                    print('server_message')
                    f.write(server_buffer)
                    f.close()
        except Exception as e:
            print(e)
        return


if __name__ == "__main__":
    t1 = threading.Thread(target=sender, args=())
    t2 = threading.Thread(target=receiver, args=())

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

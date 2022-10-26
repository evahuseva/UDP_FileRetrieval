import os.path
import socket
import time

buffer_size = 10240
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print('Socket created.')
client_socket.bind(('172.25.0.2', 4900))
print('Socket bound.')

server_address = ('172.25.0.3', 4900)

client_message = input('What do you want to send? ')
client_buffer = client_message.encode('utf-8')
client_socket.sendto(client_buffer, server_address)
print(f'Message {client_message} sent to server {server_address[0]}. ')


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


while True:
    time.sleep(0.01)
    buffer, server = client_socket.recvfrom(buffer_size)
    message = None
    try:
        message = buffer.decode('ascii')
    except:
        pass
    try:
        if message == 'NONE':
            print(f'File "{client_message}" not found. ')
            break
        elif message == 'END':
            print(f'File "{client_message}" finished loading. ')
            break
        else:
            print(f'Received part of "{client_message}": ')
            file_path = os.path.join('/files', client_message)
            file_object = open(file_path, 'ab')
            file_object.write(buffer)
            file_object.close()
            print(color.PURPLE + buffer.decode('utf-8') + color.END)
    except FileNotFoundError:
        print(f'No "{client_message}" found in this directory. ')

print('Client stopped working normally. ')

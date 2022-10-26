import os
import queue
import socket
import sys
import threading
import time


class Worker:

    def __init__(self, ipv4: str, port: int, delay: float, buffer_size: int, server: tuple):
        self.address: str = ipv4
        self.port: int = port
        self.address_and_port: tuple = (ipv4, port)
        self.delay: float = delay
        self.buffer_size: int = buffer_size
        self.server = server

        self.socket: socket.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.thread_listen: threading.Thread = None
        self.thread_respond: threading.Thread = None
        self.thread_input: threading.Thread = None
        self.continue_listen: bool = True
        self.continue_process: bool = True
        self.continue_input: bool = True

        self.queue: queue.Queue = queue.Queue()

# 'start' and 'stop' are used for threading
    def start(self):
        self.socket.bind(self.address_and_port)
        self.continue_listen = True
        self.thread_listen = threading.Thread(target=self.__listen)
        self.thread_listen.start()
        print(f'Socket up and listening at {self.address}:{self.port}.')
        self.continue_process = True
        self.thread_respond = threading.Thread(target=self.__respond)
        self.thread_respond.start()
        print(f'Ready to respond to server requests.')
        self.continue_input = True
        self.thread_input = threading.Thread(target=self.__input)
        self.thread_input.start()
        print(f'Ready to receive input.')

    def stop(self):
        self.continue_listen = False
        self.continue_process = False
        self.continue_input = False
        time.sleep(self.delay)
        if self.thread_listen is not None and self.thread_listen.is_alive():
            self.thread_listen.join(1)
        if self.thread_respond is not None:
            self.thread_listen.join(1)
        if self.thread_input is not None:
            self.thread_listen.join(1)
        exit()

# checking the buffer for received bytes
    def __listen(self):
        while self.continue_listen:
            time.sleep(self.delay)
            buffer, _ = self.socket.recvfrom(self.buffer_size)
            self.queue.put(buffer)
            print(f'Message came from server {_[0]}:{_[1]} with task id {buffer[:32].hex()} and content'
                  + f' {buffer[16:].decode("utf-8")}. ')
        print('Stopped listening. ')

# processing the operations and sending the response about actions
    def __respond(self):
        while self.continue_process:
            time.sleep(self.delay)
            server_buffer: bytes = self.queue.get(block=True)
            if server_buffer is not None:
                request_id: bytes = server_buffer[:32]
                filename: str = server_buffer[32:].decode('utf-8')
                file_path: str = os.path.join('/worker_files', filename)
                print(f'Processing request with id {request_id.hex()} and filename {filename} ')
                if os.path.exists(file_path):
                    print(f'File {file_path} found. ')
                    file_object = open(file=file_path, mode='rb')
                    while True:
                        time.sleep(self.delay)
                        file_buffer = file_object.read(self.buffer_size - 32)
                        if len(file_buffer) == 0:
                            self.__send(request_id, 'END')
                            print(f'Sent all data for {file_path}. ')
                            break
                        self.__send(request_id, file_buffer)
                        print(f'Sent data chunk for {file_path}. ')
                else:
                    print(f'File {file_path} not found. ')
                    self.__send(request_id, 'NONE')
                break
        print('Stopped responding. ')

# listening to input commands
    def __input(self):
        print('Started listening for input. ')
        while self.continue_input:
            command = input('What is your command? ').upper()
            if command.startswith('JOIN'):
                self.__join(command)
            elif command == 'LEAVE':
                self.__leave()
            elif command == 'QUIT' or command == 'EXIT' or command == 'Q':
                print('Not listening for input anymore. ')
                self.__quit()
                sys.exit()
            else:
                self.__unknown(command)
        print('Not listening for input anymore. ')

    def __join(self, command: str):
        address = command.replace('JOIN', '')
        address = address.replace(' ', '')
        if address != '':
            self.server = (address, 4916)
        self.__send(b'', 'JOIN')
        print(f'Joined server {self.server[0]}:{self.server[1]} at your behest. ')

    def __leave(self):
        self.__send(b'', 'LEAVE')
        print(f'Left server {self.server[0]}:{self.server[1]} at your behest. ')

    def __unknown(self, command: str):
        print(f'Unknown command. ')

    def __quit(self):
        print('Fare thee well. ')
        self.stop()

    def __send(self, id: bytes, message):
        message_bytes = None
        if type(message) is bytes:
            message_bytes = message
        elif type(message) is str:
            message_bytes = message.encode('ascii')
        message_bytes = id + message_bytes
        self.socket.sendto(message_bytes, self.server)

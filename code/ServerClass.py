import queue
import socket
import threading
import time
import uuid
from FileTask import FileTask


class Server:

    def __init__(self, buffer_size, ip_address, client_port, worker_port, worker_addresses: list, delay: int = 0.01):
        self.client_in_queue = queue.Queue()
        self.worker_out_queue = queue.Queue()
        self.buffer_size = buffer_size
        self.delay = delay
        self.workers = worker_addresses
        self.workers_lock = threading.Lock()
        self.tasks = {}
        self.task_lock = threading.Lock()
        self.ip_address = ip_address
        self.client_port = client_port
        self.worker_port = worker_port

        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.worker_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.client_listen_thread = threading.Thread(target=self.__client_listen)
        self.client_process_thread = threading.Thread(target=self.__client_process)
        self.worker_listen_thread = threading.Thread(target=self.__worker_listen)

    def start(self):
        self.client_socket.bind((self.ip_address, self.client_port))
        self.client_listen_thread.start()
        self.client_process_thread.start()
        print(f'Server socket up and listening for clients at {self.ip_address}:{self.client_port}. ')
        self.worker_socket.bind((self.ip_address, self.worker_port))
        self.worker_listen_thread.start()
        print(f'Server socket up and listening for workers at {self.ip_address}:{self.worker_port}. ')

# receiving the message from client
    def __client_listen(self):
        print('Client listener started. ')
        while True:
            time.sleep(self.delay)
            client_buffer, client_address_and_port = self.client_socket.recvfrom(self.buffer_size)
            client_address, client_port = client_address_and_port
            client_message = client_buffer.decode('utf-8')
            print(f'Client {client_address}:{client_port} sent message "{client_message}". ')
            task = FileTask(client_address_and_port, client_buffer, [] + self.workers.copy())
            self.client_in_queue.put(item=task)
    print('Stopped listening for clients.')

# transmitting the client message to workers
    def __client_process(self):
        while True:
            time.sleep(self.delay)
            if not self.client_in_queue.empty():
                client_task: FileTask = self.client_in_queue.get(block=True)
                print(f'Processing client {client_task.get_address()}:{client_task.get_port()} file request with id ' +
                      f'{client_task.id} and message "{client_task.get_message()}". ')
                worker_buffer = client_task.get_worker_buffer()
                client_task.workers = self.workers.copy()
                self.__task_add(client_task)
                if len(client_task.workers) > 0:
                    print('Task has workers. ')
                    for worker in client_task.workers:
                        self.worker_socket.sendto(worker_buffer, worker)
                else:
                    print('Task has no workers. ')
                    self.client_socket.sendto(b'NONE', client_task.address_and_port)
                    # self.client_in_queue.put(client_task, block=True)
        print('Stopped processing file requests.')

# receiving the response from workers
    def __worker_listen(self):
        while True:
            try:
                time.sleep(self.delay)
                worker_buffer, worker_address_and_port = self.worker_socket.recvfrom(self.buffer_size)
                self.__worker_process(worker_address_and_port, worker_buffer)
            except KeyError:
                print('KeyError happened. ')
        print('Stopped listening to workers.')

    def __task_add(self, client_task: FileTask):
        self.task_lock.acquire(blocking=True)
        self.tasks[client_task.id] = client_task
        self.task_lock.release()

    def __task_remove(self, task: FileTask):
        self.task_lock.acquire(blocking=True)
        self.tasks.pop(task.id)
        self.task_lock.release()

    def __task_worker_remove(self, worker: tuple):
        self.task_lock.acquire(blocking=True)
        for task in self.tasks:
            task.workers.remove(worker)
        self.task_lock.release()

    def __worker_add(self, worker):
        self.workers_lock.acquire(blocking=True)
        self.workers.append(worker)
        self.workers_lock.release()

    def __worker_remove(self, worker):
        self.workers_lock.acquire(blocking=True)
        self.workers.remove(worker)
        self.__task_worker_remove(worker)
        self.workers_lock.release()

    def __worker_process(self, worker: tuple, worker_buffer: bytes):
        print(f'Processing worker {worker[0]}:{worker[1]} message.')
        if len(worker_buffer) < 33:
            worker_message = worker_buffer.decode('ascii')
            if worker_message == 'JOIN':
                self.__worker_add(worker)
                print(f'Worker {worker[0]}:{worker[1]} joins the server.')
            elif worker_message == 'LEAVE':
                self.__worker_remove(worker)
                print(f'Worker {worker[0]}:{worker[1]} leaves the server.')
        else:
            task_id = uuid.UUID(hex=worker_buffer[:32].decode('ascii'))
            print(f'Worker {worker[0]}:{worker[1]} responded to task {task_id}.')
            task: FileTask = self.tasks[task_id]
            worker_buffer_content = worker_buffer[32:]
            worker_content = None
            try:
                worker_content = worker_buffer_content.decode('ascii')
            except:
                pass
            if worker_content == 'NONE':
                task.workers.remove(worker)
                print(f'Worker {worker[0]}:{worker[1]} had no file {task.get_message()}. ')
            elif worker_content == 'END':
                task.workers.clear()
                print(f'Worker {worker[0]}:{worker[1]} finished sending file {task.get_message()}. ')
            else:
                self.__client_send(task, worker_buffer_content)
                print(f'Worker {worker[0]}:{worker[1]} sent chunk of file {task.get_message()}. ')
            if len(task.workers) == 0:
                print(f'Processing task {task.id.hex} finished with result {worker_content}. ')
                self.__client_send(task, worker_buffer_content)
                self.__task_remove(task)

# sending the files, received from workers, to the client
    def __client_send(self, task: FileTask, buffer: bytes):
        self.client_socket.sendto(buffer, task.address_and_port)

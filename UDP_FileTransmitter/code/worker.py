import socket
from WorkerClass import Worker

worker = Worker(socket.gethostbyname(socket.gethostname()), 4916, 0.25, 10240, ('172.25.0.3', 4916))
worker.start()

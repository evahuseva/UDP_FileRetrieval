import uuid


class FileTask:

    def __init__(self, client_address_and_port: tuple, client_buffer: bytes, workers: list):
        self.address_and_port = client_address_and_port
        self.buffer = client_buffer
        self.id = uuid.uuid4()
        self.workers = workers.copy()

    def get_worker_buffer(self):
        return self.id.hex.encode('ascii') + self.buffer

    def get_address(self):
        return self.address_and_port[0]

    def get_port(self):
        return self.address_and_port[1]

    def get_message(self):
        return self.buffer.decode('utf-8')

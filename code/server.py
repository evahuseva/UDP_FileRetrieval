from ServerClass import Server


server_instance = Server(10240, '172.25.0.3', 4900, 4916, [('172.25.0.4', 4916), ('172.25.0.5', 4916), ('172.25.0.6', 4916)])
server_instance.start()

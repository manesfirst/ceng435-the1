import socket
import sys

import datetime

ipAddress, port = "10.10.1.2", 30000

data = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    start = datetime.datetime.now()
    sock.connect((ipAddress, port))
    sock.sendall(data.encode())

    received = str(sock.recv(1024), "utf-8")
    end = datetime.datetime.now()
    print(received)
    print(end - start)

finally:
    sock.close()


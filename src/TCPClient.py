import socket
import sys
import time

ipAddress, port = "10.10.1.2", 30000

data = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    start = str(time.time())
    sock.connect((ipAddress, port))
    sock.sendall((data + "?" + str(start)).encode())

    received = str(sock.recv(1024), "utf-8")
    print(received)


finally:
    sock.close()


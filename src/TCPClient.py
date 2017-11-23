import socket
import sys
import time
"""This is the TCP client script. It is put to T1 node of the remote servers"""
ipAddress, port = "10.10.1.2", 30000 #IP address of the Gateway server's T1 link and the port that Gateway's TCP server listens to.

data = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    start = str(time.time())
    sock.connect((ipAddress, port))
    sock.sendall((data + "?" + str(start)).encode()) #We just open a socket, combine the current time with the destination with our
                                                     #  delimeter '?', then send the encoded string from the socket, and wait for a data to arrive from the further nodes.

    received = str(sock.recv(1024), "utf-8")
    print(received)


finally:
    sock.close()


import socket
import socketserver
import time

class RouterT2Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip().decode()
        print(data)
        receivedTime = float(data.split("?")[1])
        currentTime = time.time()
        print(currentTime-receivedTime)
        print(data.decode() + " I'm T3 Destination!")

        self.request.sendall("This is T3!".encode())


ipAddress = "10.10.5.2"
port = 21000
TCPserver = socketserver.TCPServer((ipAddress, port), RouterT2Server)
TCPserver.serve_forever()
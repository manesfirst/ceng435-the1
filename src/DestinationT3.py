import socket
import socketserver
import time

class DestinationT3Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip().decode()
        # print(data)
        receivedTime = float(data.split("?")[1])
        currentTime = time.time()
        print(currentTime-receivedTime)
        # print(data + " I'm T3 Destination!")

        self.request.sendall("This is T3!".encode())


ipAddress = "10.10.5.2"
port = 21000
TCPserver = socketserver.TCPServer((ipAddress, port), DestinationT3Server)
try:
    TCPserver.serve_forever()

except KeyboardInterrupt:
    TCPserver.server_close()

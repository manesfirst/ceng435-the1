import socket
import socketserver


class RouterT2Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        print(data.decode() + " I'm T2 Router!")
        self.handleTCPredirection(data)


    def handleTCPredirection(self,data):
        ipAddress, port = "10.10.5.2", 21000 #The port that T2 listens

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request.sendall(received.encode())

        finally:
            sock.close()

ipAddress = "10.10.3.2"
port = 27500
TCPserver = socketserver.TCPServer((ipAddress, port), RouterT2Server)
TCPserver.serve_forever()
import socket
import socketserver


class RouterU2Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        print(data.decode() + " I'm U2 router!")
        self.handleUDPredirection(data)


    def handleUDPredirection(self, data):
        ipAddress, port = "10.10.6.2", 20000

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request[1].sendto(received.encode(), self.client_address)

        finally:
            sock.close()






ipAddress = "10.10.4.2"
port = 28000
RouterServer = socketserver.UDPServer((ipAddress, port), RouterU2Server)
try:
    RouterServer.serve_forever()

except KeyboardInterrupt:
    RouterServer.server_close()

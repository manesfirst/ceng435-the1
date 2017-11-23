import socket
import socketserver


class RouterU2Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        print(data.decode() + " I'm U2 router!")
        self.handleUDPredirection(data)


    def handleUDPredirection(self, data):
        ipAddress, port = "10.10.6.2", 20000 #IP address of the U3 and the port that U3 listens to.

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #The code is very similar to Gateway's UDP server. When request comes, i
                                                                # t prints the data and 'I'm U2 router!' string, opens a socket to next node, send the data and wait for response

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

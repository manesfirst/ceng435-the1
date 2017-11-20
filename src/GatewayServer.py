import socket
import socketserver
import threading


class GatewayServerUDP(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        # socket = self.request[1]
        # print("{} wrote:".format(self.client_address[0]))
        destination = data.decode().split("?")[0]
        print(data.decode() + " I'm Gateway UDP server!")
        if('U' in destination):
            self.handleUDPredirection(data)
            pass

        else:
            self.handleTCPredirection(data)


    def handleTCPredirection(self, data):

        ipAddress, port = "10.10.1.2", 30000

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request[1].sendto(received.encode(), self.client_address)

        finally:
            sock.close()


    def handleUDPredirection(self, data):
        ipAddress, port = "10.10.4.2", 28000 #the port that U2 listens

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request[1].sendto(received.encode(), self.client_address)
        finally:
            sock.close()


class GatewayServerTCP(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        print(data.decode() + "I'm gateway TCP server!")
        destination = data.decode().split("?")[0]
        if('T' in destination):
            self.handleTCPredirection(data)
            pass
        else:
            self.handleUDPredirection(data)


    def handleTCPredirection(self,data):
        ipAddress, port = "10.10.3.2", 27500 #The port that T2 listens

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request.sendall(received.encode())

        finally:
            sock.close()

    def handleUDPredirection(self, data):
        ipAddress, port = "10.10.2.2", 29000

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request.sendall(received.encode())

        finally:
            sock.close()


def udpServer():
    ipAddress = "10.10.2.2"
    port = 29000
    UDPserver = socketserver.UDPServer((ipAddress,port),GatewayServerUDP)
    try:
        UDPserver.serve_forever()

    except KeyboardInterrupt:
        UDPserver.server_close()


def tcpServer():
    ipAddress = "10.10.1.2"
    port = 30000
    TCPserver = socketserver.TCPServer((ipAddress, port), GatewayServerTCP)
    try:
        TCPserver.serve_forever()

    except KeyboardInterrupt:
        TCPserver.server_close()





if __name__ == "__main__":
    udpServerThread = threading.Thread(target=udpServer)
    tcpServerThread = threading.Thread(target=tcpServer)

    udpServerThread.start()
    tcpServerThread.start()

    udpServerThread.join()
    tcpServerThread.join()
















import socket
import socketserver
import threading


class GatewayServerUDP(socketserver.BaseRequestHandler):
    """This is the UDP server for gateway server. It inherits a base class, which is in the socketserver library. It opens a new thread for each connection, so that the programmer doesn't have to deal with too much threading stuff"""
    def handle(self):
        data = self.request[0].strip() #This part does the actual reading of the data. Most of the underlying stuff is handled by the socketserver.
                                       # When request comes, this 'handle' function is invoked, then rest is left to programmer
        destination = data.decode().split("?")[0] # Split the input with the delimeter that we put.
        print(data.decode() + " I'm Gateway UDP server!")
        if('U' in destination):
            self.handleUDPredirection(data) #The destination is U3.

        else:
            self.handleTCPredirection(data) #Destination is TCP


    def handleTCPredirection(self, data):

        ipAddress, port = "10.10.1.2", 30000 #For handling TCP destination requests that are sent from U1, we just send another request to our own TCP server locally, and it does the rest of the job.

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8") #We are waiting for the response from furher nodes, and when the response comes, we direct it to the socket that the initial request came from.
            self.request[1].sendto(received.encode(), self.client_address)

        finally:
            sock.close()


    def handleUDPredirection(self, data):
        ipAddress, port = "10.10.4.2", 28000 ##IP address of the U2 and the port that U2 listens to.

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request[1].sendto(received.encode(), self.client_address)
        finally:
            sock.close()


class GatewayServerTCP(socketserver.BaseRequestHandler):
    """This is the TCP counterpart of UDP server, again, it is inherited from the same class."""
    def handle(self):
        data = self.request.recv(1024).strip()
        print(data.decode() + "I'm gateway TCP server!")
        destination = data.decode().split("?")[0]
        if('T' in destination):
            self.handleTCPredirection(data) #It's destination is T3
            pass
        else:
            self.handleUDPredirection(data) #Destination is U3


    def handleTCPredirection(self,data):
        ipAddress, port = "10.10.3.2", 27500 #IP address of the T2 and the port that T2 listens to.

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((ipAddress, port))
            sock.sendall(data)

            received = str(sock.recv(1024), "utf-8")
            self.request.sendall(received.encode())

        finally:
            sock.close()

    def handleUDPredirection(self, data):
        ipAddress, port = "10.10.2.2", 29000 #Redirect the request to UDP server

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
    UDPserver = socketserver.UDPServer((ipAddress,port),GatewayServerUDP) #We use these two functions to open threads, and
                                                                          # run the server class. We added KeybordInterrup exception in order to catch Ctrl+C signal that has been sent from terminal
    try:
        UDPserver.serve_forever()

    except KeyboardInterrupt:
        UDPserver.server_close()


def tcpServer():
    ipAddress = "10.10.1.2"
    port = 30000
    TCPserver = socketserver.TCPServer((ipAddress, port), GatewayServerTCP)#Initilizer for the server. It takes a tuple with two arguements, ip address and port, and class that should serve as a server
    try:
        TCPserver.serve_forever()

    except KeyboardInterrupt:
        TCPserver.server_close()





if __name__ == "__main__":
    udpServerThread = threading.Thread(target=udpServer) #Starting point of the threads and the server.
    tcpServerThread = threading.Thread(target=tcpServer)

    udpServerThread.start()
    tcpServerThread.start()

    udpServerThread.join()
    tcpServerThread.join()
















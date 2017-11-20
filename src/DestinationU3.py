import socketserver
import time

class DestinationU3Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip().decode()
        # print(data)
        receivedTime = float(data.split("?")[1])
        currentTime = time.time()
        print(currentTime-receivedTime)
        # print(data + " I'm U3 destination!")

        self.request[1].sendto("This is U3!".encode(), self.client_address)


ipAddress = "10.10.6.2"
port = 20000
RouterServer = socketserver.UDPServer((ipAddress, port), DestinationU3Server)
try:
    RouterServer.serve_forever()

except KeyboardInterrupt:
    RouterServer.server_close()

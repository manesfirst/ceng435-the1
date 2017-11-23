import socketserver
import time

class DestinationU3Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip().decode() #These are basically the same server with Routers. They just don't send the data any more further, these start to send data bask to listeners.
        receivedTime = float(data.split("?")[1]) #Takes the time from client node, converts it to float, and find the difference between that and current time.
        currentTime = time.time()
        print(currentTime-receivedTime)

        self.request[1].sendto("This is U3!".encode(), self.client_address)


ipAddress = "10.10.6.2"
port = 20000
UDPserver = socketserver.UDPServer((ipAddress, port), DestinationU3Server)
try:
    UDPserver.serve_forever()

except KeyboardInterrupt:
    UDPserver.server_close()

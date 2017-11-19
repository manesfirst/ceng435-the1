import socketserver


class DestinationU3Server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        print(data.decode() + " I'm U3 destination!")

        self.request[1].sendto("This is U3!".encode(), self.client_address)


ipAddress = "10.10.6.2"
port = 20000
RouterServer = socketserver.UDPServer((ipAddress, port), DestinationU3Server)
RouterServer.serve_forever()

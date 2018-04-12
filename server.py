# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
ACCEPT_IP = '192.168.1.13'

class Connect(object):

    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('socket cannot be created')
        server_address = ('192.168.1.2', PORT)
        #print('starting up: ' + server_address)
        self.sock.bind(server_address)
        self.sock.listen(1)

    def listen(self):
        while True:
            connection, client_address = self.sock.accept()
            print 'Connected by', client_address

            try:
            	if client_address[0] != ACCEPT_IP:
            		connection.sendall('GO AWAY!!')
            		connection.close()

                data = connection.recv(1024)
                print(data)
                connection.sendall(data)
            finally:
                connection.close()

def main():
    connect = Connect()
    connect.listen()

if __name__=='__main__':
    main()

# Echo server program
import socket
import datetime

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
                if self.write(data):
                    connection.sendall('data logged: '+ data)
                else:
                    connection.sendall('error logging data: '+ data)
            finally:
                connection.close()

    def write(self, string):
        try:
            file=open("/Users/harijsme/Documents/temperature_logs/test_"+datetime.datetime.now().strftime("%d.%m.%Y")+".txt",mode="a")
            file.write(string+'\n')
            file.close()
            return True
        except:
            return False

def main():
    connect = Connect()
    connect.listen()

if __name__=='__main__':
    main()

# Echo client program
import socket
import time
import random

HOST = '192.168.1.2'    # The remote host
PORT = 50007              # The same port as used by the server

class Connect(object):

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('connecting to host')
        sock.connect((HOST, PORT))
        return sock

    def send(self, command):
        sock = self.connect()
        recv_data = ""
        data = True

        print('sending: '+ command)
        sock.sendall(command)

        while data:
            data = sock.recv(1024)
            recv_data += data
            print('response: '+ recv_data)
        return recv_data


connect = Connect()
starttime=time.time()

while True:
  send_text = str(random.random())
  connect.send(send_text)
  time.sleep(5.0 - ((time.time() - starttime) % 5.0))

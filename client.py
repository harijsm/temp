# Echo client program
import socket
import time
import random
import datetime
import os

HOST = '192.168.1.2'      # The remote host
PORT = 50007              # The same port as used by the server
BACKUP_DIR = './backup_temp_logs/'
TIMEOUT = 15.0

class Connect(object):

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('')
        print('connecting to host')
        sock.connect((HOST, PORT))
        return sock

    def send(self, command):
        try:
            sock = self.connect()
            recv_data = ""
            data = True

            print('sending: '+ command)
            sock.sendall(command)

            while data:
                data = sock.recv(1024)
                recv_data += data
            return 'response: '+ recv_data
        except:
            return 'Connection refused!! error logging data: '+command
    def write(self, string):
        try:
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)

            file=open(BACKUP_DIR+datetime.datetime.now().strftime("%d.%m.%Y")+".txt",mode="a")
            file.write(string+'\n')
            file.close()
            return 'OK!'
        except:
            return 'ERROR:'


connect = Connect()
starttime=time.time()

while True:
    send_text = str(random.random())
    response = connect.send(send_text)
    if "error logging data" in response:
        status = connect.write(send_text)
        print response
        print (status+ " writing backup log on SD: "+ send_text)
    else:
        print response
  
    time.sleep(TIMEOUT - ((time.time() - starttime) % TIMEOUT))

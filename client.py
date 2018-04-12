# Echo client program
import socket
import time
import datetime
import os
import glob

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

HOST = '192.168.1.2'      # The remote host
PORT = 50007              # The same port as used by the server
BACKUP_DIR = './backup_temp_logs/'
TIMEOUT = 15.0

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')

if len(device_folder) > 0:
    device_file = device_folder[0] + '/w1_slave'
else:
    device_file = False

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

def read_temp_raw():
    if device_file == False:
        return False

    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()

    return lines

def read_temp():
    lines = read_temp_raw()
    if lines == False:
        return False

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp = float(temp_string) / 1000.0
        return temp

connect = Connect()
starttime=time.time()

while True:
    try:
        send_text = read_temp()
        if send_text != False:
            response = connect.send(send_text)
        else:
            response = "error reading temp from DS18B20"
    except:
        response = "error reading temp from DS18B20"
    
    if "error logging data" in response:
        status = connect.write(send_text)
        print response
        print (status+ " writing backup log on SD: "+ send_text)
    else:
        print response
  
    time.sleep(TIMEOUT - ((time.time() - starttime) % TIMEOUT))

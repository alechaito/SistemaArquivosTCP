import socket
import time
import traceback
from _thread import *
import threading
import sys

def main():
    tcp = TCP()
    tcp.server()


class TCP():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = '127.0.0.1'  
        self.PORT = 5000
        self.BUFFER = 1024
        self.THREADS = []

    def server(self):
        orig = (self.HOST, self.PORT)
        try:
            self.socket.bind((self.HOST, self.PORT))
        except:
            print("Bind failed. Error : " + str(sys.exc_info()))
            sys.exit()

        self.socket.listen(5)
        while(True):
            con, cliente = self.socket.accept()
            client = Client(self.HOST, self.PORT, con) 
            client.start()

    
class Client(threading.Thread):
    def __init__(self, ip, port, con): 
        threading.Thread.__init__(self)
        self.ip = ip 
        self.port = port
        self.con = con
        self.WELCOME_MSG = "Welcome to the file server.."
        print("[+] New server socket thread started for "+ip+":"+str(port))
    
    def run(self):    
        print("[+] Connection from : "+self.ip+":"+str(self.port))
        
        self.con.send(self.WELCOME_MSG.encode())

        data = "init"
        while len(data):
            data = self.con.recv(1024)
            print("Client sent :"+ str(data) )




main()
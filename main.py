import socket
import time
import traceback
from _thread import *
import threading
import sys
import os
import shutil
import socket
from distutils.dir_util import copy_tree

threads = []
output = []
mutex = thread.allocate_lock()

def main():
    tcp = TCP()
    tcp.server()


class TCP():
    def __init__(self):
        print("Initializing...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.HOST = '127.0.0.1'  
        self.PORT = 5000
        self.BUFFER = 1024

    def server(self):
        orig = (self.HOST, self.PORT)
        self.socket.bind((self.HOST, self.PORT))

        self.socket.listen(5)
        while(True):
            con, cliente = self.socket.accept()
            client = Client(self.HOST, self.PORT, con) 
            client.start()
            threads.append(client)
        
        for t in threads:
            t.join()
    
class Client(threading.Thread):
    def __init__(self, ip, port, con): 
        threading.Thread.__init__(self)
        self.ip = ip 
        self.port = port
        self.con = con
        self.MSG = "init"
        self.WELCOME_MSG = "[+] Welcome to the file server.. \n"
        self.INVOKE_ERROR = "[+] Command Not Found... \n"
        self.INVOKE_SUCCESS = "[+] Command succes... \n"
        print("[+] New server socket thread started for "+ip+":"+str(port))
    
    def run(self):
        mutex.acquire()
        print("[+] Connection from : "+self.ip+":"+str(self.port))
        self.con.send(self.WELCOME_MSG.encode())
        while len(self.MSG):
            self.MSG = self.con.recv(1024).decode().rstrip()
            print("[+] Client sent :"+ self.MSG )
            self.invoke()
        mutex.release()
    
    def invoke(self):
        ##COMMAND PATTERN: CMD,FILE_NAME,TO_PATH -> Example: mv,test.php,/var/www/
        command = self.MSG.split(" ")
        ##CREATE FILE -> Command pattern: mkdir,file_or_directory_name,type
        if(command[0] == 'mkdir'):
            if(command[2] == 0): ##FILE
                os.mknod(command[1])
                self.con.send(self.INVOKE_SUCCESS.encode())
            else: ##DIR
                os.mkdir(command[1])
                self.con.send(self.INVOKE_SUCCESS.encode())
        ##REMOVE FILE -> Command pattern: rm file_or_directory_name type
        elif(command[0] == 'rm'):
            if(command[2] == 0):
                ## TRY REMOVE FILE
                try: 
                    os.remove(command[1])
                    self.con.send(self.INVOKE_SUCCESS.encode())
                except:
                    print("[+] Error...")
            else:
                ## TRY REMOVE DIRECTORY
                try:
                    shutil.rmtree(command[1])
                    self.con.send(self.INVOKE_SUCCESS.encode())
                except:
                    print("[+] Error...")
        ##RENAME FILE -> Command pattern: mv file_name new_file_name
        elif(command[0] == 'mv'):
            os.rename(comamnd[1], command[2])
            self.con.send(self.INVOKE_SUCCESS.encode())
        ##LIST FILE -> Command pattern: ls dir
        elif(command[0] == 'ls'):
            result = str(os.listdir(command[1]))+"\n"
            self.con.send(result.encode())
            self.con.send(self.INVOKE_SUCCESS.encode())
        ##COPY FILE OR DIRECTORY -> Command pattern: cp from to type
        elif(command[0] == 'cp'):
            if(command[3] == 0): # IS FILE
                shutil.copy2(command[1], command[2])
                reself.con.send(self.INVOKE_SUCCESS.encode())
            else: # IS DIRECTORY
                copy_tree(command[1], command[2])
                self.con.send(self.INVOKE_SUCCESS.encode())
        ##LIST FILE
        elif(command[0] == 'quit'):
            sys.kill()
        else:
            self.con.send(self.INVOKE_ERROR.encode())



main()

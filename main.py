import socket



HOST = '198.50.194.112'     # Endereco IP do Servidor
PORT = 7171           # Porta que o Servidor esta
MSG = "TEST"

def main():
    tcp = TCP()
    
    tcp.client()
    tcp.server()


class TCP():

    def __init__(self):
        self.HOST = '198.50.194.112'  
        self.PORT = 7171 
        self.MSG = "TEST"

    def client(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.HOST, self.PORT)
        tcp.connect(dest)
        print('Para sair use CTRL+X')
        tcp.send (self.MSG.encode())

    def server(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.HOST, self.PORT)
        tcp.bind(orig)
        tcp.listen(1)
        while True:
            con, cliente = tcp.accept()
            print('Concetado por', cliente)
            while True:
                msg = con.recv(1024)
                if not msg: break
                print(cliente, msg)
            print('Finalizando conexao do cliente', cliente)
            con.close()







main()
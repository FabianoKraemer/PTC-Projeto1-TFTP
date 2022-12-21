# UDP multicast examples, Hugo Vincent, 2005-05-14.
from socket import *

class TFTPClient():

        def __init__(self, server:str, port:int, timeout:int):
                self.Estados = Enum('Estados', 'ocioso init rx esc') # Estados possíveis da ME
                self.estado = self.Estados.ocioso
                self.sock = socket(AF_INET, SOCK_DGRAM)
                self.IP = '127.0.0.1'
                self.porta = 5555
                self.server = server
                self.port = port  #geralmente usada a 69,
                self.testebind = False;
                

        def send(self, data:str, port=5555, addr='127.0.0.1'):
                self.sock.sendto(data, (addr, port))

        def recebe(self, port=5555, addr="127.0.0.1", buf_size=1024): 
                if(self.testebind == False): 
                        self.sock.bind(('', self.porta)) 
                        self.testebind = True                           
                data, enderecos = self.sock.recvfrom(1024)               
                # enderecos[0] = ip
                # enderecos[1] = porta
                #print(data)
                self.sock.close
                return data

        def handle(self, data:str):
                # lê uma linha do teclado
                dados = sys.stdin.readline()

                # converte para bytes, necessário somente
                # nesta aplicação de teste, que lê do terminal
                dados = dados.encode('utf8')

                # monta o quadro
                self.monta_quadro(dados)                


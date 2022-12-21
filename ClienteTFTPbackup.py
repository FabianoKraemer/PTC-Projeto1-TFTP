# UDP multicast examples, Hugo Vincent, 2005-05-14.
from enum import Enum
from socket import *
import sys
import poller

class  ClienteTFTP(poller.Callback):

    #def __init__(self, server:str, port:int, timeout:int):
    def __init__(self, TouR, address:str, porta:int, timeout:int):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        #poller.Callback.__init__(self, self.socket, timeout)        
        poller.Callback.__init__(self, sys.stdin, timeout)
        #self.Estados = Enum('Estados','menu init rx tx') # Estados possíveis da ME
        self.Estados = Enum('Estados', 'init Tx0 Tx1 Tx2 Rx0 Rx1 Rx2 rx tx')
        self.estado = self.Estados.init
        self.server_padrao = address
        self.porta_padrao = porta
        #self.serverRX = '127.0.0.1'
        #self.portaRX = 5555
        self.testebind = False
        self.dado = bytearray()
        self.ToR = TouR # False pra transmitir, True pra receber
        #self.sched = poller.Poller
        self.enable_timeout()

    def envia(self):
        self.estado = self.Estados.tx
        # lê uma linha do teclado
        print('digite o texto: ')
        self.dado = sys.stdin.readline()
        self.dado = self.dado.encode('utf-8')
        self.socket.sendto(self.dado, (self.server_padrao, self.porta_padrao))
        #self.dado = data
        #self.handle()
        #self.sched.adiciona(self)
        #self.sched.despache()
        #self.enable()

    def recebe(self, port=5555, addr="127.0.0.1", buf_size=1024): 
        if(self.testebind == False): 
                self.socket.bind(('', self.porta_padrao)) 
                self.testebind = True  
        msg, addr = self.socket.recvfrom(1024)
        if(msg == bytearray()):
            print('msg vazia (linha 48)')
            return False
        self.estado = self.Estados.rx
        self.dado = msg
        #self.sched.adiciona(self)
        #self.sched.despache()
        #self.enable()
        #self.enable_timeout()
        return True

    def handle(self):       
        #if (self.estado == self.Estados.rx):
        if (self.ToR == True):
            print('handle Rx')
            if(self.recebe() == True):
                self.RX()  
        #if (self.estado == self.Estados.menu):
            #self.opcoes()
        #if (self.estado == self.Estados.tx):
        if (self.ToR == False):    
            print('handle Tx')
            self.TX()

    ''' baseados na MEF do link https://moodle.ifsc.edu.br/mod/page/view.php?id=660116&forceview=1
        e https://moodle.ifsc.edu.br/mod/page/view.php?id=660158&forceview=1
    '''
    def handleTx0(self):
        print('handle TX0')

    def handleTx1(self):
        print('handle TX1')

    def handleTx2(self):
        print('handle TX2')

    def handleRx0(self):
        print('handle RX0')  

    def handleRx1(self):
        print('handle RX1')   

    def handleRx2(self):
        print('handle RX2')

    def TX(self):
        print('digite o texto: ')
        self.dado = sys.stdin.readline()
        self.dado = self.dado.encode('utf-8')
        self.socket.sendto(self.dado, (self.server_padrao, self.porta_padrao))
        self.estado = self.Estados.tx

    def RX(self):              
        print(self.dado)
        self.socket.close                       

    def handle_timeout(self): 
        print('timeout ainda não implementado')
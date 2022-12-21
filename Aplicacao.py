import sys
import poller
from ClienteTFTP import *

class Aplicacao(poller.Callback):

    def __init__(self, timeout: int = 0):
        poller.Callback.__init__(self, timeout=0)

    def opcoes(self):
        while(True):
            print('Digite uma opção (1 para transmitir, 2 para receber): ')
            # lê uma linha do teclado
            opcao = input()
            if (opcao == '1'):
                while(True):
                    print('opcao1')
                    #protocolo.envia()
            elif (opcao == '2'):
                print('opcao 2')
                #protocolo.recebe()
            else: 
                print('opção errada, digite novamente.')


    def handle(self):
        print('teste handle aplicacao')
        self.opcoes()
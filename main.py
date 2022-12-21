import poller
import sys
from ClienteTFTP import *
from Aplicacao import Aplicacao


Timeout = 3  # 10 segundos
address = '127.0.0.1'
porta = 5555

print('O IP padrão está como 127.0.0.1 e a porta 5555. O timeout está com 10 segundos')
print('Digite uma opção e pressione Enter duas vezes(1 para transmitir, 2 para receber): ')
RouT = False

clienteTFTP = ClienteTFTP(RouT, address, porta, Timeout)

while(True):
    # lê uma linha do teclado    
    opcao = input()       
    if (opcao == '1'):
        #clienteTFTP.estado = clienteTFTP.Estados.tx
        #clienteTFTP.envia()
        nomeArquivo = "arquivoEnvio.txt" #Digite aqui o nome do arquivo
        clienteTFTP.envia(nomeArquivo)
        RouT = False
        break
    elif (opcao == '2'):    
        endereco_arquivo = "receitaDeBolo" #Digite aqui o nome do arquivo      
        RouT = True        
        clienteTFTP.recebe(endereco_arquivo)
        # Cria o Poller e registra os callbacks
        #sched = poller.Poller()
        #sched.adiciona(clienteTFTP)
        # Entrega o controle ao Poller
        #sched.despache()        
        break
    else: 
        print('opção errada, digite novamente.') 

# cria objeto TFTP
#clienteTFTP = ClienteTFTP('127.0.0.1', 5555, Timeout)
#clienteTFTP = ClienteTFTP(Timeout)
#menu = Aplicacao(Timeout)

#clienteTFTP = ClienteTFTP(RouT, address, porta, Timeout)

# Cria o Poller e registra os callbacks
#sched = poller.Poller()
#sched.adiciona(clienteTFTP)
#sched.adiciona(menu)

#clienteTFTP.opcoes()

# Entrega o controle ao Poller
#sched.despache()

'''
while(True):
    print('Digite uma opção (1 para transmitir, 2 para receber): ')
    # lê uma linha do teclado
    opcao = input()
    if (opcao == '1'):
        #while(True):
        clienteTFTP.envia()
    elif (opcao == '2'):
        clienteTFTP.recebe()
    else: 
        print('opção errada, digite novamente.')
'''
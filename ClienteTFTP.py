# UDP multicast examples, Hugo Vincent, 2005-05-14.
from enum import Enum
from socket import *
import sys
import poller
from WRQ import *
from RRQ import *
from Ack import *
from Data import *

class  ClienteTFTP(poller.Callback):

    def __init__(self, TouR, address:str, porta:int, timeout:int):
        self.Estados = Enum('Estados', 'init Tx0 Tx1 Tx2 Rx0 Rx1 Rx2 rx tx') # Estados possíveis da MEF
        self.estado = self.Estados.init
        self.socket = socket(AF_INET, SOCK_DGRAM)      
        poller.Callback.__init__(self, self.socket, timeout)
        self.server_padrao = address # usando o 127.0.0.1
        self.porta_padrao = porta # Usando a 5555
        self.porta_recebida = porta # Porta recebida pelo outro lado
        #self.serverRX = '127.0.0.1'
        #self.portaRX = 5555
        self.testebind = False
        self.dado = bytearray() # Teste para transmitir textos
        self.buffer = bytearray() # Armazena os dados recebidos pelo socket  
        self.nomeArquivo = None # Nome do arquivo para baixar ou enviar     
        self.ToR = TouR # False pra transmitir, True pra receber, usado para testes de envio de texto
        #self.sched = poller.Poller
        self.qtde_timeout = 0 # testes quantidade vezes refazer por timeout
        self.sequencia = 0 # variável correspondente a MEF do professor pra sinalizar a sequência
        self.qtde_pacotes = 0 #variável correspondente a MEF do professor para verificar a quantidade de pacotes
        self.msg = None # Variável do dado/pacote que será enviado ou recebido     
        self.buffer_quadro_N = None # Armazena os dados do número do quadro correspondente
        self.split_conteudo = None # Variavel pra armazenar num vetor os blocos de 512 bytes, testando

        self.enable_timeout()

    def envia(self, caminho_arquivo:str): # Envia o arquivo escolhido pelo caminho dele
        self.nomeArquivo = caminho_arquivo
        with open(self.nomeArquivo, "rb") as file_object:
            conteudo = file_object.read() # Carrega o arquivo pra calcular o tamanho
        #print('conteudo: ', conteudo)
        self.qtde_pacotes = int(1+(len(conteudo)/512)) # Calcula a quantidade de pacotes que serão transmitidos       
        # Testando
        self.split_conteudo = [conteudo[i:i + 512] for i in range(0, len(conteudo), 512)] # Divide o conteudo do arquivo em partes de 512 bytes, adaptado de semestres anteriores
        self.msg = WRQ(caminho_arquivo).getQuadro() # Cria e retorna o quadro para ser enviado para o servidor
        print('Tamanho conteudo para transmitir: ', str(len(conteudo)))
        print('Quantidade de pacotes: ', self.qtde_pacotes)
        print('Mensagem enviada: ', self.msg)
        self.socket.sendto(self.msg, (self.server_padrao, self.porta_recebida)) # Envia o WRQ
        self.estado = self.Estados.Tx0 # Ativa o estado Tx0 na MEF
        self.sequencia = 1     
        self.enable()
        self.enable_timeout()
        sched = poller.Poller() # Cria o objeto do poller
        sched.adiciona(self) # Se registra no Callback do Poller
        sched.despache() # Entrega o controle para o Poller

    def recebe(self, end_arquivo): 
        self.nomeArquivo = end_arquivo
        self.msg = RRQ(end_arquivo).getQuadro()
        self.sequencia = 1
        self.estado = self.Estados.Rx0 # Ativa o estado Rx0 na MEF       
        self.socket.sendto(self.msg, (self.server_padrao, self.porta_padrao)) # Envia o RRQ com o nome do arquivo
        self.enable()
        self.enable_timeout()
        sched = poller.Poller() # Cria o objeto do poller
        sched.adiciona(self) # Se registra no Callback do Poller
        sched.despache() # Entrega o controle para o Poller

    def handle(self):
        if (self.testebind == False): 
                #self.socket.bind(('', self.porta_padrao)) 
                self.testebind = True          
        msg, addr = self.socket.recvfrom(1024)  
        self.server_padrao = addr[0]
        self.porta_recebida = addr[1] 
        #if (self.estado == self.Estados.rx):

        # MEF:
        if self.estado == self.Estados.Tx0:
            self.handleTx0(msg)        
        if self.estado == self.Estados.Tx1:
            self.handleTx1(msg)    
        if self.estado == self.Estados.Tx2:
            self.handleTx2(msg)    
        if self.estado == self.Estados.Rx0:
            self.handleRx0(msg)        
        if self.estado == self.Estados.Rx1:
            self.handleRx1(msg)    
        if self.estado == self.Estados.Rx2:
            self.handleRx2(msg)  

    ''' baseados na MEF do link https://moodle.ifsc.edu.br/mod/page/view.php?id=660116&forceview=1
        e https://moodle.ifsc.edu.br/mod/page/view.php?id=660158&forceview=1
    '''
    def handleTx0(self, dados):
        print('handle TX0')
        ack = b'\x00\x04' # Código do ACK da RFC
        error = b'\x00\x05' # Código de erro da RFC

        if (dados[:2] == ack and int.from_bytes(dados[2:4], "big") == 0): # Primeiro Ack recebido, precisa ser seq 0
            self.qtde_timeout = 0
            self.buffer_quadro_N = Data(self.sequencia, self.split_conteudo.pop(0)).getQuadro() # Retira o 1° bloco de 512 bytes do conteudo splitado            
            if (self.qtde_pacotes > 1): # Vai para o Tx1 caso haja mais de 1 pacote
                self.estado = self.Estados.Tx1 # Continua enviando enquanto tiver mais de 1 pacote
            else:
                self.estado = self.Estados.Tx2 # Caso tenha só um pacote para transferir, vai para o estado Tx2
            self.socket.sendto(self.buffer_quadro_N, (self.server_padrao, self.porta_recebida))
        elif (dados[:2] == error):
            print("Deu erro no Tx0, código do erro: ")  #print para teste
            print(dados[4:len(dados)-2].decode())  #print da mensagem de erro de acordo com a RFC do protocolo
            self.estado = self.Estados.init # Volta para o estado inicial
            self.disable()
            self.disable_timeout()

    def handleTx1(self, dados):
        print('handle TX1')
        ack = b'\x00\x04' # Código do ACK da RFC
        error = b'\x00\x05' # Código de erro da RFC

        if (dados[:2] == ack and int.from_bytes(dados[2:4], "big") == self.sequencia): # Segundo Ack recebido, precisa ser seq 1
            self.qtde_timeout = 0
            self.sequencia += 1
            self.buffer_quadro_N = Data(self.sequencia, self.split_conteudo.pop(0)).getQuadro() # Retira o bloco de 512 bytes do conteudo splitado          
            self.socket.sendto(self.buffer_quadro_N, (self.server_padrao, self.porta_recebida))

        elif (dados[:2] == error):
            print("Deu erro no Tx1, código do erro: ")  #print para teste
            print(dados[4:len(dados)-2].decode())  #print da mensagem de erro de acordo com a RFC do protocolo
            self.estado = self.Estados.init # Volta para o estado inicial
            self.disable()
            self.disable_timeout()

    def handleTx2(self, dados):
        print('handle TX2')
        ack = b'\x00\x04' # Código do ACK da RFC
        error = b'\x00\x05' # Código de erro da RFC

        if (dados[:2] == ack and int.from_bytes(dados[2:4], "big") == self.sequencia):  # # Segundo Ack recebido, precisa ser igual a self.sequencia
            self.qtde_timeout = 0
            self.estado = self.Estados.init
            self.disable()
            self.disable_timeout()
        elif (dados[:2] == error):
            print("Deu erro no Tx2, código do erro: ")  # print para teste
            print(dados[4:len(dados)-2].decode())  # print da mensagem de erro de acordo com a RFC do protocolo
            self.estado = self.Estados.init # Volta para o estado inicial
            self.disable()
            self.disable_timeout()

    def handleRx0(self, dados):
        print('handle RX0')  
        data = b'\x00\x03' # Código de data da RFC
        error = b'\x00\x05' # Código de erro da RFC

        if (dados[:2] == data and int.from_bytes(dados[2:4], "big") == self.sequencia): # Recebendo dado e conferindo com a sequência equivalente          
            self.buffer += dados[4:len(dados) + 1] #adiciona o conteudo util do data recebido ao buffer
            self.qtde_timeout = 0
            self.sequencia += 1
            self.socket.sendto(Ack(self.sequencia).getQuadro(), (self.server_padrao, self.porta_recebida))

            if (len(dados) < 512): # Se for menor que 512, é o ultimo quadro
                self.estado = self.Estados.Rx2 
            else: #(len(dados) == 512):
                self.estado = self.Estados.Rx1  # Há mais dados para transmitir, vai pro Rx1
        elif (dados[:2] == error):
            print("Erro no Rx0, código: ")
            print(dados[4:len(dados)-2].decode()) # Imprime o código do erro
            self.estado = self.Estados.init # Volta para o estado inicial
            self.disable()
            self.disable_timeout()

    def handleRx1(self, dados):
        print('handle RX1')   
        data = b'\x00\x03' # Código de data da RFC
        error = b'\x00\x05' # Código de erro da RFC

        if (dados[:2] == data):  # Dado recebido
            if(int.from_bytes(dados[2:4], "big") == self.sequencia): # # Recebendo dado e conferindo com a sequência equivalente
                self.socket.sendto(Ack(self.sequencia).getQuadro(), (self.server_padrao, self.porta_recebida)) # Envia Ack de recebimento
                self.qtde_timeout = 0
                self.buffer += dados[4:len(dados) + 1] # Adiciona o novo quadro aos anteriores          
                if (len(dados) < 512):
                    self.estado = self.Estados.Rx2  # Se for menor que 512, é o ultimo quadro
                else:
                    self.sequencia += 1 # Tem mais pacotes
            else:
                # Sequencia dos dados errada, reenvia ack atual
                self.socket.sendto(Ack(self.sequencia-1).getQuadro(), (self.server_padrao, self.porta_recebida)) # Reenvia Ack
                self.qtde_timeout = 0
        elif (dados[:2] == error):
            dados_recebidos = dados[4:len(dados) - 2].decode()
            print("Erro no RX1, codigo: ", dados_recebidos)  # Mensagem de erro
            self.estado = self.Estados.init
            self.disable()
            self.disable_timeout()

    def handleRx2(self, dados):
        print('handle RX2')
        data = b'\x00\x03' # Código de data da RFC
        error = b'\x00\x05' # Código de erro da RFC

        if (dados[:2] == data): # Recebeu dado final
            if(int.from_bytes(dados[2:4], "big") == self.sequencia): # Recebendo dado e conferindo com a sequência equivalente
                self.socket.sendto(Ack(self.sequencia).getQuadro(), (self.server_padrao, self.porta_recebida)) # Enviando o ack correspondente
                self.estado = self.Estados.init # Voltando ao estado ocioso
                self.disable()
                self.disable_timeout()
        elif (dados[:2] == error): # Erro
            dados_recebidos = dados[4:len(dados) - 2].decode()
            print("Erro no Rx2, codigo: ", dados_recebidos)  # Mensagem de erro
            self.estado = self.Estados.init # Voltando ao estado ocioso
            self.disable()
            self.disable_timeout()

    # Função para teste de envio de msgs pelo terminal
    def TX(self):
        print('digite o texto: ')
        self.dado = sys.stdin.readline()
        self.dado = self.dado.encode('utf-8')
        self.socket.sendto(self.dado, (self.server_padrao, self.porta_padrao))
        self.estado = self.Estados.tx

    # Função para teste de recebimento de msgs pelo terminal
    def RX(self):              
        print(self.dado)
        self.socket.close                       

    def handle_timeout(self): 

        self.qtde_timeout += 1
        
        # Volta ao estado ocioso
        if (self.estado == self.Estados.Rx0 or self.estado == self.Estados.Rx1 or self.estado == self.Estados.Tx0):            
            if (self.qtde_timeout > 5): 
                self.buffer.clear()
                self.qtde_timeout = 0
                self.estado = self.Estados.init
                self.disable()
                self.disable_timeout()

        # Caso der timeout sem enviar pela primeira vez, tenta novamente 5 vezes
        elif (self.estado == self.Estados.Tx1 or self.estado == self.Estados.Tx2):
            if (self.qtde_timeout < 5): #verifica se encerra o cliente ou tenta de novo
                self.socket.sendto(self.buffer, (self.server_padrao, self.porta_recebida))
                print("Tentando reenvio no timeout pela tentativa ", self.sequencia)
            else:
                print("Perda de comunicação com servidor. Encerrando o envio.")
                self.qtde_timeout = 0
                self.estado = self.Estados.init
                self.disable()
                self.disable_timeout()

        elif (self.estado == self.Estados.Rx2): # GuardTimer da MEF
            print("Rx2, Guardtimer")
            with open(self.nomeArquivo, 'wb') as file_object:
                file_object.write(self.buffer)
                file_object.close()                

            self.estado = self.Estados.init # Voltando ao estado ocioso
            self.disable() # Desabilitando o sched
            self.disable_timeout() # Desabilitando o timeout
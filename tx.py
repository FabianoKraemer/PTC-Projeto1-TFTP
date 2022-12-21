import socket
import sys
from TFTPClientteste import *

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

#sock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))

teste_TFTP = TFTPClient('127.0.0.1', 5555)

while True:
    # lê uma linha do teclado
    dados = sys.stdin.readline()

    # converte para bytes, necessário somente
    # nesta aplicação de teste, que lê do terminal
    dados = dados.encode('utf8')

    data = teste_TFTP.send(dados)
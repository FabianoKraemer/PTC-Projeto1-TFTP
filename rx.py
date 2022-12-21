import socket
from TFTPClientteste import *

UDP_IP = "127.0.0.1"
UDP_PORT = 5555

#sock = socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#teste_TFTP = TFTPClient('127.0.0.1', 5555, 10)

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #data = teste_TFTP.recebe()

    print("Mensagem recebida: ", data)
class WRQ():

    def __init__(self, nomeArquivo):
        opCode = bytearray([0, 2]) # Código do WRQ conforme RFC
        self.nomeArquivo = bytearray(nomeArquivo, 'utf-8') # converte a string nomeArquivo para bytearray com codificação uft-8
        zero_byte = bytearray([0]) # byte delimitador
        #Mode = bytearray('octet', 'netascii') 
        Mode = "netascii"
        Mode = bytes(Mode, 'utf-8') # mode octeto utf-8, seguindo a RFC       
        self.quadro = opCode + self.nomeArquivo + zero_byte + Mode + zero_byte # forma a mensagem do quadro     
        
        #opcode = p[0:2].decode('ASCII')
        #nameEnd = p.find(b'\0', start=2)
        #filename = p[2:nameEnd].decode('ASCII')
        #modeEnd = p.find(b'\0', start=nameEnd+1)
        #mode = p[nameEnd+1:modeEnd].decode('ASCII')
    # Retorna o quadro criado
    def getQuadro(self):
        return self.quadro
        
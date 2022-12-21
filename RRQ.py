class RRQ():

    def __init__(self, nomeArquivo):
        opcode = bytearray([0, 1])  # Código do RRQ conforme RFC 
        self.nomeArquivo = bytearray(nomeArquivo, 'utf-8')  # converte a string nomeArquivo para bytearray com codificação uft-8
        zero_byte = bytearray([0]) # byte delimitador
        mode = bytearray('octet', 'utf-8')  # mode octeto utf-8, seguindo a RFC        
        self.quadro = (opcode + self.nomeArquivo + zero_byte + mode + zero_byte)  # forma a mensagem do quadro  

    # Retorna o quadro criado
    def getQuadro(self):
        return self.quadro 
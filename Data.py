class Data():

    def __init__(self, codData, data):
        opcode = bytearray([0, 3]) # Opcode do Data conforme RFC do TFTP
        self.codData = codData.to_bytes(2, 'big') # Codifica para 2 bytes
        self.quadro = (opcode + self.codData + data) # forma a mensagem do quadro 

    # Retorna o quadro criado
    def getQuadro(self):
        return self.quadro
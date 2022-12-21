class Ack():

    def __init__(self, codAck):
        opcode = bytearray([0, 4]) # Opcode do ACK conforme RFC do TFTP
        self.numBloco = codAck.to_bytes(2, 'big') # Codifica para 2 bytes
        self.quadro = (opcode + self.codAck) # forma a mensagem do quadro  

    # Retorna o quadro criado
    def getQuadro(self):
        return self.quadro
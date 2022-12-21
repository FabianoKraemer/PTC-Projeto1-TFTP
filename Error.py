class Error():

    def __init__(self, codError):
        opcode = bytearray([0, 5]) # Opcode do Error conforme RFC do TFTP
        self.codError = bytearray([0, codError]) # Converte para bytearray
        msgError = bytearray(self.getMsgError(codError), 'utf-8') # Recebe a msg de erro correspondente e converte pra utf-8
        zero_byte = bytearray([0]) # Byte delimitador
        self.pacote = (opcode + self.codError + msgError + zero_byte) # Forma a mensagem do quadro 

    def getMsgError(self, codError):
        return {
            1: 'File not found.',
            2: 'Access violation.',
            3: 'Disk full or allocation exceeded.',
            4: 'Illegal TFTP operation.',
            5: 'Unknown transfer ID.',
            6: 'File already exists.',
            7: 'No such user.',
            8: 'Not defined, see error message (if any).'
        }[codError] #funcao para retornar a string de erro

    def getPacote(self):
        return self.pacote #retorna o pacote criado
#!/usr/bin/env python3

import poller
import sys,time

# declara um Callback capaz de fazer leitura do teclado, e com tempo limite
class CallbackStdin(poller.Callback):
    
    def __init__(self, tout:float):
        'tout: tempo limite de espera, em segundos'
        poller.Callback.__init__(self, sys.stdin, tout)
        self._cnt = 0

    def handle(self):
        'O tratador do evento leitura'
        l = sys.stdin.readline()
        print('Lido:', l)
        self._cnt = 0

    def handle_timeout(self):
        'O tratador de evento timeout'
        self._cnt += 1
        print(f'Timeout: cnt={self._cnt}')
        if self._cnt == 3:
            # desativa o timeout deste callback, e também o evento leitura !
            self.disable_timeout()         
            self.disable()

####################################   

# instancia um callback
cb = CallbackStdin(3)

# cria o poller (event loop)
sched = poller.Poller()

# registra o callback no poller
sched.adiciona(cb)

# entrega o controle pro loop de eventos
sched.despache()
import random

from .carta import Carta
from .naipe import Naipe


class Baralho:
    def __init__(self):
        print("Instanciou Baralho")
        self._cartas = []
        self.reiniciar_baralho()
        print(self._cartas)

    def reiniciar_baralho(self):
        for numero in range(1,14):
            ouro = Carta(numero, Naipe.OUROS) 
            copa = Carta(numero, Naipe.COPAS)
            pau = Carta(numero, Naipe.PAUS)
            espada = Carta(numero, Naipe.ESPADAS)
            self._cartas.extend([ouro, copa, pau, espada])

    def get_cartas(self) -> list[Carta]:
        pass


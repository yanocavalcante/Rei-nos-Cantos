import random

from .carta import Carta
from .naipe import Naipe


class Baralho:
    def __init__(self):
        print("Instanciou Baralho")
        self._cartas = []
        self.reiniciar_baralho()

    def reiniciar_baralho(self):
        for numero in range(1,14):
            ouro = Carta(numero, Naipe.OUROS) 
            copa = Carta(numero, Naipe.COPAS)
            pau = Carta(numero, Naipe.PAUS)
            espada = Carta(numero, Naipe.ESPADAS)
            self._cartas.extend([ouro, copa, pau, espada])

    def get_cartas(self) -> list[Carta]:
        return self._cartas
    
    def get_carta_codigo(self, codp) -> Carta:      #Retorna uma instância de carta que tenha o código passado
        for carta in self._cartas:
            if carta._codigo == codp:
                return carta 


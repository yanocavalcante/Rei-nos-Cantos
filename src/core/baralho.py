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
            ouro = Carta(numero, Naipe.DIAMONDS) 
            copa = Carta(numero, Naipe.HEARTS)
            pau = Carta(numero, Naipe.CLUBS)
            espada = Carta(numero, Naipe.SPADES)
            self._cartas.extend([ouro, copa, pau, espada])

    def get_cartas(self) -> list[Carta]:
        return self._cartas
    
    def get_carta_codigo(self, codp) -> Carta:      #Retorna uma instância de carta que tenha o código passado
        print("Cartas do Baralho:", self._cartas)
        for carta in self._cartas:
            if carta.get_codigo() == codp:
                return carta 


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
    
    def get_carta_codigo(self, codp) -> Carta:      #Retorna uma instância de carta baseado num código fornecido
        for carta in self._cartas:
            if carta.get_codigo() == codp:
                return carta 
            
    def get_carta_por_nome_imagem(self, nome_imagem_carta: str):
        #formato esperado: "{rank}_of_{suit}"
        rank, suit = nome_imagem_carta.split("_of_")

        for carta in self._cartas:
            if carta.get_numero() == int(rank) and carta.get_naipe().name.lower() == suit.lower():
                return carta
    
    def get_codigo_cartas(self, cartas_selecionadas) -> list:   #Retorna uma lista de códigos com base nas instâncias de carta fornecidas
        lista_codigos = []
        for carta in cartas_selecionadas:
            lista_codigos.append(carta.get_codigo())
        return lista_codigos



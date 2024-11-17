from .pilha import Pilha
from .baralho import Baralho
import random


class Mesa:
    def __init__(self):
        print("Instanciou Mesa")
        cantos = []
        self._pilhas = [Pilha(str(i)) for i in range(4)]
        self._monte = Pilha("M")
        for i in range(4):
            codp = f"C{i}"
            canto = Pilha(codp)
            cantos.append(canto)
        self._pilhas.extend(cantos)

    def limpar_mesa(self):
        pass

    def remover_carta_monte(self, carta):
        pass

    def comprar_carta_monte(self):
        pass

    def embaralhar_monte(self) -> list:
        cartas_do_baralho = self._baralho.get_cartas()
        random.shuffle(cartas_do_baralho)
        cartas_do_monte = cartas_do_baralho[:32]
        cartas_restantes = cartas_do_baralho[32:]
        for carta in cartas_do_monte:
            self._monte.adicionar_cartas_pilha(carta)
        return cartas_restantes

    def colocar_cartas_mesa(self, lista_cartas: list) -> list:
        count = 0
        for pilha in self._pilhas:
            if count == 4:
                return
            pilha.adicionar_cartas_pilha([lista_cartas.pop(0)])
            count += 1
    
    def instanciar_baralho(self):
        self._baralho = Baralho()

    def distribuir_cartas_jogador(self, lista_cartas: list, jogador) -> list:
        for i in range(7):
            jogador.adicionar_nova_carta(lista_cartas.pop(0))
        return lista_cartas
    
    def get_monte(self) -> Pilha:
        return self._monte
    
    def get_pilhas(self) -> list:
        return self._pilhas
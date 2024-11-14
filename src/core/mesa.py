from .pilha import Pilha


class Mesa:
    def __init__(self):
        print("Instanciou Mesa")
        self._pilhas = [Pilha() for _ in range(8)]
        self._monte = Pilha()

    def limpar_mesa(self):
        pass

    def remover_carta_monte(self, carta):
        pass

    def comprar_carta_monte(self):
        pass

    def embaralhar_monte(self, lista_cartas: list) -> list:
        pass

    def colocar_cartas_mesa(self, lista_cartas: list) -> list:
        pass
    
    def instanciar_baralho(self):
        pass

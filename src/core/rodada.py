from .jogador import Jogador


class Rodada:
    def __init__(self):
        jogador_local = Jogador()
        jogador_remoto = Jogador()

    def comparar_jogador(self, jogador: Jogador) -> bool:
        pass

    def alterar_comprou_carta(self):
        pass

    def verificar_compra(self):
        pass

    def get_jogador(self) -> Jogador:
        pass

    def adicionar_jogador(jog_contrario: Jogador) -> Jogador:
        pass

    def set_jogador(self, prox_jogador: Jogador) -> Jogador:
        pass

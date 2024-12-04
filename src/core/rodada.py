from .jogador import Jogador


class Rodada:
    def __init__(self):
        self._jogador = None
        self._comprou_carta = False

    def comparar_jogador(self, jogador: Jogador) -> bool:
        if self._jogador.get_id() != jogador.get_id():
            return False
        else:
            return True

    def alterar_comprou_carta(self):
        self._comprou_carta = not (self._comprou_carta)

    def verificar_compra(self) -> bool:
        return self._comprou_carta

    def get_jogador(self) -> Jogador:
        return self._jogador

    def set_jogador(self, prox_jogador: Jogador) -> Jogador:
        self._jogador = prox_jogador

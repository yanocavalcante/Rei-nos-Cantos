class Partida:
    def __init__(self, jogador_local: Jogador, jogador_remoto: Jogador, mesa: Mesa, rodada_atual: Rodada):
        pass

    def abandonar_partida(self):
        pass

    def obtem_status(self):
        pass

    def receive_start(self, jogadores: list):
        pass

    def obter_status_partida(self) -> str:
        pass

    def restaurar_estado_inicial(self):
        pass

    def reiniciar_vitoria(self):
        pass

    def passar_a_vez(self):
        pass

    def pegar_jog_contrario(self, jogador: Jogador) -> Jogador:
        pass

    def desistir(self):
        pass

    def comecar_partida(self, jogadores: list):
        pass

    def avaliar_vencedor(self) -> bool:
        pass

    def mover_cartas(self):
        pass

    def jogar_carta(self):
        pass

    def comprar_carta(self):
        pass

    def colocar_rei(self):
        pass

    def receber_jogada(self):
        pass

    def verificar_inicio(self) -> bool:
        pass

    def obter_jogada(self, jogada: dict):
        pass

    def encerrar_partida(self):
        pass

    def get_encerrou(self) -> bool:
        pass


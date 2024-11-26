from .rodada import Rodada
from .mesa import Mesa
from .jogador import Jogador

class Partida:
    def __init__(self):
        print("Instanciou Partida")
        self._rodada_atual = Rodada()
        self._mesa = Mesa()
        self._jogador_remoto = Jogador()
        self._jogador_local = Jogador()
        self._partida_em_andamento = False

    def abandonar_partida(self):
        pass

    def obtem_status(self):
        pass

    def receive_start(self, jogadores: list):
        self._jogador_local.reset()
        id_jog = jogadores[1][1]
        self._jogador_local.inicializar(id_jog)
        self._jogador_remoto.reset()
        id_jog = jogadores[0][0]
        self._jogador_remoto.inicializar(id_jog)
        self._rodada_atual.set_jogador(self._jogador_remoto)

    def obter_status_partida(self) -> str:
        pass

    def restaurar_estado_inicial(self):
        pass

    def reiniciar_vitoria(self):
        pass

    def passar_a_vez(self):
        pass

    def pegar_jog_contrario(self, jogador):
        pass

    def desistir(self):
        pass

    def comecar_partida(self, jogadores: list):
        pilhas_mesa = self._mesa.get_pilhas()

        self._jogador_local.reset()
        self._jogador_local.inicializar(jogadores[0][1])

        self._jogador_remoto.reset()
        self._jogador_remoto.inicializar(jogadores[1][1])

        self._rodada_atual.set_jogador(self._jogador_local)
        self.instanciar_baralho()
        self.set_partida_em_andamento()

        inicio = {
            'tipo_jogada': "inicio",
            'pilha_adiciona': None,
            'pilha_remove': None,
            'carta': None,
            'cartas_monte': self._mesa.get_monte().get_codigo_cartas(),
            'cartas_pilha_0': pilhas_mesa[0].get_codigo_cartas(),
            'cartas_pilha_1': pilhas_mesa[1].get_codigo_cartas(),
            'cartas_pilha_2': pilhas_mesa[2].get_codigo_cartas(),
            'cartas_pilha_3': pilhas_mesa[3].get_codigo_cartas(),
            'cartas_canto_0': None,
            'cartas_canto_1': None,
            'cartas_canto_2': None,
            'cartas_canto_3': None,
            'cartas_jogador_local': self._jogador_local.get_codigos_mao(),
            'cartas_jogador_remoto': self._jogador_remoto.get_codigos_mao(),
            'match_status': None
        }

        return inicio

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

    def set_partida_em_andamento(self):
        if self._partida_em_andamento == True:
            self._partida_em_andamento = False
        elif self._partida_em_andamento == False:
            self._partida_em_andamento = True

    def get_partida_em_andamento(self) -> bool:
        return self._partida_em_andamento
    
    def instanciar_baralho(self):
        self._mesa.instanciar_baralho()

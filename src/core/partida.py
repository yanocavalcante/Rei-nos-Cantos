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
        cartas_restantes = self._mesa.embaralhar_monte()

        cartas_jogadores = self._mesa.colocar_cartas_mesa(cartas_restantes)

        self._mesa.distribuir_cartas_jogador(cartas_jogadores[:7], self._jogador_remoto)
        self._mesa.distribuir_cartas_jogador(cartas_jogadores[7:], self._jogador_local)
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
            'match_status': "next",
            'venceu': "false"
        }
        return inicio

    def avaliar_vencedor(self) -> bool:
        pass

    def mover_cartas(self):
        pilhas_mesa = self._mesa.get_pilhas()
        mover = {
            'tipo_jogada': "mover",
            'pilha_adiciona': None,
            'pilha_remove': None,
            'cartas': None,
            'match_status': "next",
        }
        return mover

    def jogar_carta(self):
        pass

    def comprar_carta(self):
        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                return {"boolean": True, "mensagem": "Não é possível comprar mais de uma carta!", "carta": None }, None
            else:
                carta_comprada = self._mesa.comprar_carta_monte()
                self._jogador_local.adicionar_cartas(carta_comprada)
                self._rodada_atual.alterar_comprou_carta()
                compra = {                  #Comprar Carta tem que ser jogada porque precisa atualizar o monte do jogador remoto também
                    'tipo_jogada': "compra",
                    'cartas': carta_comprada.get_codigo(),
                }
                return {"boolean": False, "mensagem": None, "carta": carta_comprada}, compra
        else:
            return {"boolean": True, "mensagem": "Não é possível comprar carta fora do turno", "carta": None}, None

    def colocar_rei(self):
        pass

    def receber_jogada(self, jogada):
        if jogada['tipo_jogada'] == 'inicio':
            self.instanciar_baralho()
            self._mesa.get_pilha_codigo('M').adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas_monte']))
            self._mesa.get_pilha_codigo('0').adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas_pilha_0']))
            self._mesa.get_pilha_codigo('1').adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas_pilha_1']))
            self._mesa.get_pilha_codigo('2').adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas_pilha_2']))            
            self._mesa.get_pilha_codigo('3').adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas_pilha_3']))
            self._jogador_local.adicionar_cartas(self._mesa.get_cartas_codigo(jogada['cartas_jogador_remoto']))
            self._jogador_remoto.adicionar_cartas(self._mesa.get_cartas_codigo(jogada['cartas_jogador_local']))   #Lembrar que os pontos de vista sempre se invertem
        else:
            if jogada['tipo_jogada'] == 'mover':
                self._mesa_get_pilha_codigo(jogada['pilha_adiciona']).adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas']))
                self._mesa_get_pilha_codigo(jogada['pilha_remove']).retirar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas']))
            elif jogada['tipo_jogada'] == 'rei_no_canto' or jogada['tipo_jogada'] == 'jogar':
                self._mesa_get_pilha_codigo(jogada['pilha_adiciona']).adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas']))
            elif jogada['tipo_jogada'] == 'passar':
                nova_rodada = Rodada()
                self.set_rodada_atual(nova_rodada)
            elif jogada['tipo_jogada'] == 'desistir':
                pass

    def verificar_inicio(self) -> bool:     #APAGAR NO DIAGRAMA
        pass

    def obter_jogada(self, jogada: dict):   #APAGAR NO DIAGRAMA
        pass

    def set_partida_em_andamento(self):
        if self._partida_em_andamento == True:
            self._partida_em_andamento = False
        elif self._partida_em_andamento == False:
            self._partida_em_andamento = True

    def get_partida_em_andamento(self) -> bool:
        return self._partida_em_andamento
    
    def instanciar_baralho(self):
        return self._mesa.instanciar_baralho()

    def set_rodada_atual(self, rodada):
        self._rodada_atual = rodada

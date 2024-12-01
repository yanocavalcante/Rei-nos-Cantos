from .rodada import Rodada
from .mesa import Mesa
from .jogador import Jogador

class Partida:
    def __init__(self):
        print("Instanciou Partida")
        self._rodada_atual = Rodada()
        self._mesa = Mesa()
        self._partida_em_andamento = False

    def abandonar_partida(self):
        pass

    def obtem_status(self):
        pass

    def receive_start(self, jogadores: list):
        self._jogador_local = Jogador(jogadores[1][0], jogadores[1][1])
        self._jogador_remoto = Jogador(jogadores[0][0], jogadores[0][1])
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

        self._jogador_local = Jogador(jogadores[0][0], jogadores[0][1])
        self._jogador_remoto = Jogador(jogadores[1][0], jogadores[1][1])
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

    def mover_cartas(self, cartas, pilha1, pilha2):
        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                if self._mesa.get_pilha_codigo(pilha2).verifica_colocacao_carta(cartas):
                    mover = {              
                    'tipo_jogada': "mover",
                    'cartas': cartas.get_codigo(),
                    'pilha_remove': pilha1,
                    'pilha_adiciona': pilha2,
                    'match_status': 'next',
                    }
                    return {"mensagem": "Moveu cartas!", "carta": None }, mover
                else:
                    return {"mensagem": "Movimento Inválido!", "carta": None}, None
            else:
                return {"mensagem": "Não é possível mover cartas antes de comprar uma carta!", "carta": None}, None
        else:
            return {"mensagem": "Não é possível mover cartas fora do turno", "carta": None}, None

    def jogar_carta(self):
        pass

    def comprar_carta(self):
        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                return {"mensagem": "Não é possível comprar mais de uma carta!", "carta": None }, None
            else:
                carta_comprada = self._mesa.comprar_carta_monte()
                self._jogador_local.adicionar_cartas([carta_comprada])
                self._rodada_atual.alterar_comprou_carta()
                compra = {                  #Comprar Carta tem que ser jogada porque precisa atualizar o monte do jogador remoto também
                    'tipo_jogada': "compra",
                    'cartas': carta_comprada.get_codigo(),
                    'match_status': 'next',
                }
                return {"mensagem": "Comprou Carta!", "carta": carta_comprada}, compra
        else:
            return {"mensagem": "Não é possível comprar carta fora do turno", "carta": None}, None

    def colocar_rei(self, rei, canto):
        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                if self._mesa.get_baralho().get_carta_codigo(rei).verificar_rei():
                    if self._mesa.get_pilha_codigo(canto).verifica_canto(): 
                        if self._mesa.get_pilha_codigo(canto).verifica_colocacao_carta(rei):
                            self._jogador_local.remover_carta(rei)
                            self._mesa.get_pilha_codigo(canto).adicionar_cartas_pilha([self._mesa.get_baralho().get_carta_codigo(rei)])
                            rei_no_canto = {              
                            'tipo_jogada': "rei_no_canto",
                            'carta': rei,
                            'pilha_adiciona': canto,
                            'match_status': 'next',
                            }
                            return {"mensagem": "Colocou Rei no Canto!", "carta": None }, rei_no_canto
                        else:
                            return {"mensagem": "Movimento Inválido!", "carta": None }, None
                    else:
                        return {"mensagem": "Pilha escolhida não é Canto!", "carta": None}, None        #Acho que eu não preciso verificar se é canto
                else:
                    return {"mensagem": "Carta escolhida não é Rei!", "carta": None}, None                    
            else:
                return {"mensagem": "Não é possível colocar Rei no Canto antes de comprar uma carta!", "carta": None}, None
        else:
            return {"mensagem": "Não é possível colocar Rei no Canto fora do turno", "carta": None}, None

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
                self._mesa.get_pilha_codigo(jogada['pilha_adiciona']).adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas']))
                self._mesa.get_pilha_codigo(jogada['pilha_remove']).retirar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas']))
            elif jogada['tipo_jogada'] == 'rei_no_canto' or jogada['tipo_jogada'] == 'jogar':
                self._mesa.get_pilha_codigo(jogada['pilha_adiciona']).adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas']))
                self._jogador_remoto.remover_carta(self._mesa.get_baralho().get_carta_codigo(jogada['carta']))
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

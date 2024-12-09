from .rodada import Rodada
from .mesa import Mesa
from .jogador import Jogador

class Partida:
    def __init__(self):
        print("Instanciou Partida")
        self._rodada_atual = Rodada()
        self._mesa = Mesa()
        self._partida_em_andamento = False

    def receive_start(self, jogadores: list[Jogador]):
        self._jogador_local = Jogador(jogadores[1][0], jogadores[1][1])
        self._jogador_remoto = Jogador(jogadores[0][0], jogadores[0][1])
        self._rodada_atual.set_jogador(self._jogador_remoto)

    def passar_a_vez(self):
        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                nova_rodada = Rodada()
                nova_rodada.set_jogador(self._jogador_remoto)
                self.set_rodada_atual(nova_rodada)
                passar = {              
                            'tipo_jogada': "passar",
                            'match_status': 'next',
                        }
                return {"mensagem": "Você passou a vez!"}, passar
            else:
                return {"mensagem": "Não é possível passar a vez antes de comprar uma carta!"}, None
        else:
            return {"mensagem": "Não é possível passar a vez fora do turno"}, None

    def desistir(self):
        self.toggle_partida_em_andamento()
        desistir = {              
                'tipo_jogada': "desistir",
                'match_status': 'interrupted',
                }
        return desistir

    def comecar_partida(self, jogadores: list[Jogador]):
        pilhas_mesa = self._mesa.get_pilhas()

        self._jogador_local = Jogador(jogadores[0][0], jogadores[0][1])
        self._jogador_remoto = Jogador(jogadores[1][0], jogadores[1][1])
        self._rodada_atual.set_jogador(self._jogador_local)
        
        self.instanciar_baralho()
        cartas_restantes = self._mesa.embaralhar_monte()

        cartas_jogadores = self._mesa.colocar_cartas_mesa(cartas_restantes)

        self._mesa.distribuir_cartas_jogador(cartas_jogadores[:7], self._jogador_remoto)
        self._mesa.distribuir_cartas_jogador(cartas_jogadores[7:], self._jogador_local)
        self.toggle_partida_em_andamento()

        inicio = {
            'tipo_jogada': "inicio",
            'pilha_adiciona': None,
            'pilha_remove': None,
            'cartas': None,
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

    def avaliar_vencedor(self, jogador: Jogador) -> bool:
        if jogador.sem_cartas():
            self.toggle_partida_em_andamento()
            return True
        else:
            return False

    def mover_cartas(self, carta: str, pilha1: str, pilha2: str) -> dict:
        carta_selecionada = self._mesa._baralho.get_carta_por_nome_imagem(carta)
        pilha_selecionada_1 = self._mesa.get_pilha_codigo(pilha1)
        pilha_selecionada_2 = self._mesa.get_pilha_codigo(pilha2)
        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                if pilha_selecionada_2.verifica_colocacao_carta(carta_selecionada):
                    index = pilha_selecionada_1.get_cartas().index(carta_selecionada)
                    cartas_selecionadas = pilha_selecionada_1.get_cartas()[index:]
                    pilha_selecionada_1.retirar_cartas_pilha(cartas_selecionadas)
                    pilha_selecionada_2.adicionar_cartas_pilha(cartas_selecionadas)
                    mover = {              
                    'tipo_jogada': "mover",
                    'cartas': self._mesa.get_baralho().get_codigo_cartas(cartas_selecionadas),
                    'pilha_remove': pilha1,
                    'pilha_adiciona': pilha2,
                    'match_status': 'next',
                    }
                    return {"mensagem": "Moveu cartas!"}, mover
                else:
                    return {"mensagem": "Movimento Inválido!"}, None
            else:
                return {"mensagem": "Não é possível mover cartas antes de comprar uma carta!"}, None
        else:
            return {"mensagem": "Não é possível mover cartas fora do turno"}, None

    def jogar_carta(self, nome_carta: str, pilha: str) -> dict:
        pilha_selecionada = self._mesa.get_pilha_codigo(pilha)
        carta = self._jogador_local.get_carta_por_nome_imagem(nome_carta)

        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                if pilha_selecionada.verifica_colocacao_carta(carta):
                    self._jogador_local.remover_carta(carta)
                    pilha_selecionada.adicionar_cartas_pilha(carta)
                    if self.avaliar_vencedor(self._jogador_local):
                        jogar_carta = {
                            'tipo_jogada': "jogar",
                            'cartas': carta.get_codigo(),
                            'pilha_adiciona': pilha_selecionada.get_codigo(),
                            'match_status': "finished",
                            'venceu': 'True',
                        }
                    else:
                        jogar_carta = {
                            'tipo_jogada': "jogar",
                            'cartas': carta.get_codigo(),
                            'pilha_adiciona': pilha_selecionada.get_codigo(),
                            'match_status': "next",
                            'venceu': 'False',
                        }
                    return {"mensagem": "Colocou carta na mesa!"}, jogar_carta
                else:
                    return {"mensagem": "Movimento inválido!"}, None
            else:
                return {"mensagem": "Não é possível jogar carta antes de comprar uma carta!"}, None
        else:
            return {"mensagem": "Não é possível jogar carta fora do turno!"}, None

    def comprar_carta(self):
        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                return {"mensagem": "Não é possível comprar mais de uma carta!"}, None
            else:
                carta_comprada = self._mesa.comprar_carta_monte()
                self._jogador_local.adicionar_cartas([carta_comprada])
                self._rodada_atual.alterar_comprou_carta()
                compra = {                  #Comprar Carta tem que ser jogada porque precisa atualizar o monte do jogador remoto também
                    'tipo_jogada': "compra",
                    'cartas': carta_comprada.get_codigo(),
                    'pilha_remove': 'M',
                    'match_status': 'next',
                }
                return {"mensagem": "Comprou Carta!"}, compra
        else:
            return {"mensagem": "Não é possível comprar carta fora do turno"}, None

    def colocar_rei(self, nome_carta: str, codp: str):
        pilha = self._mesa.get_pilha_codigo(codp)
        carta = self._jogador_local.get_carta_por_nome_imagem(nome_carta)

        if self._rodada_atual.comparar_jogador(self._jogador_local):
            if self._rodada_atual.verificar_compra():
                if carta.verificar_rei():
                    if pilha.verifica_canto(): 
                        if pilha.verifica_colocacao_carta(carta):
                            self._jogador_local.remover_carta(carta)
                            pilha.adicionar_cartas_pilha(carta)
                            if self.avaliar_vencedor(self._jogador_local):
                                rei_no_canto = {              
                                'tipo_jogada': "rei_no_canto",
                                'carta': carta,
                                'pilha_adiciona': codp,
                                'match_status': 'finished',
                                'venceu': 'True'
                                }
                            else:
                                rei_no_canto = {              
                                    'tipo_jogada': "rei_no_canto",
                                    'cartas': carta.get_codigo(),
                                    'pilha_adiciona': codp,
                                    'match_status': 'next',
                                    'venceu': 'False'
                                }
                            return {"mensagem": "Colocou Rei no Canto!"}, rei_no_canto
                        else:
                            return {"mensagem": "Movimento Inválido!"}, None
                    else:
                        return {"mensagem": "Pilha escolhida não é Canto!"}, None        #Acho que eu não preciso verificar se é canto
                else:
                    return {"mensagem": "Carta escolhida não é Rei!"}, None                    
            else:
                return {"mensagem": "Não é possível colocar Rei no Canto antes de comprar uma carta!"}, None
        else:
            return {"mensagem": "Não é possível colocar Rei no Canto fora do turno"}, None

    def receber_jogada(self, jogada: dict):
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
                self._jogador_remoto.remover_carta((self._mesa.get_cartas_codigo(jogada['cartas'])))
                self._mesa.get_pilha_codigo(jogada['pilha_adiciona']).adicionar_cartas_pilha(self._mesa.get_cartas_codigo(jogada['cartas']))
            
                if jogada['venceu'] == 'True':
                    self.toggle_partida_em_andamento()
            elif jogada['tipo_jogada'] == 'passar':
                nova_rodada = Rodada()
                nova_rodada.set_jogador(self._jogador_local)
                self.set_rodada_atual(nova_rodada)

            elif jogada['tipo_jogada'] == 'compra':
                self._mesa.get_pilha_codigo(jogada['pilha_remove']).retirar_cartas_pilha(self._mesa.get_cartas_codigo([jogada['cartas']]))

    def toggle_partida_em_andamento(self):
        self._partida_em_andamento = not(self._partida_em_andamento)

    def get_partida_em_andamento(self) -> bool:
        return self._partida_em_andamento
    
    def instanciar_baralho(self) -> object:
        return self._mesa.instanciar_baralho()

    def set_rodada_atual(self, rodada):
        self._rodada_atual = rodada

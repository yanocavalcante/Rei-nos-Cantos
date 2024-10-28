class Jogador:
    def __init__(self, cartas: list, nome: str, id: str, venceu_partida = False, sua_vez = False):
        pass

    def reset(self):
        pass

    def inicializar(self, id_jog): #Não entendi a funcionalidade dessa func. Porque o primeiro param eh um id que jah temos?
        pass

    def troca_turno(self):
        pass

    def adicionar_noca_carta(self, carta: Carta):
        pass

    def sem_cartas(self) -> boolean:
        pass

    def distribuir_cartas(self, lista_cartas: list) -> list: 
        #Quase crtz que essas funcs "distribuir" não deveriam ser de Jogador
        pass

    def distribuir_cartas(self, cartas_restantes: list):
        pass

    def get_mao(self) -> list:
        pass

class Jogador:
    def __init__(self):
        self._cartas =[]

    def reset(self):
        pass

    def inicializar(self, id_jog):
        pass

    def troca_turno(self):
        pass

    def adicionar_nova_carta(self, carta):
        pass

    def sem_cartas(self) -> bool:
        pass

    def distribuir_cartas(self, lista_cartas: list) -> list: 
        #Quase crtz que essas funcs "distribuir" não deveriam ser de Jogador
        pass

    def distribuir_cartas(self, cartas_restantes: list):
        pass

    def get_mao(self) -> list:
        return self._cartas
    
    def get_codigos_mao(self) -> list:
        lista_codigos = []
        for carta in self._cartas:
            lista_codigos.append(carta.get_codigo())
        return lista_codigos

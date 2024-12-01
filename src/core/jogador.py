class Jogador:
    def __init__(self, nome, id):
        self._cartas = []
        self._nome = nome
        self._id = id
        self._venceu_partida = False        

    def reset(self):
        pass

    def troca_turno(self):
        pass

    def adicionar_cartas(self, cartas: list):
        for carta in cartas:
            self._cartas.append(carta)
    
    def remover_carta(self, carta_a_remover):
        if carta_a_remover in self._cartas:
            self._cartas.remove(carta_a_remover)


    def sem_cartas(self) -> bool:
        pass

    def distribuir_cartas(self, lista_cartas: list) -> list: 
        #Quase crtz que essas funcs "distribuir" não deveriam ser de Jogador
        pass

    def distribuir_cartas(self, cartas_restantes: list):
        pass

    def get_mao(self) -> list:
        return self._cartas
    
    def get_id(self):
        return self._id
    
    def get_codigos_mao(self) -> list:
        lista_codigos = []
        for carta in self._cartas:
            lista_codigos.append(carta.get_codigo())
        return lista_codigos
    
    def get_carta_por_nome_imagem(self, nome_imagem_carta: str):
        #formato esperado: "{rank}_of_{suit}"
        rank, suit = nome_imagem_carta.split("_of_")

        for carta in self._cartas:
            if carta.get_numero() == int(rank) and carta.get_naipe().name.lower() == suit.lower():
                return carta
        return None 


class Jogador:
    def __init__(self, nome, id):
        self._cartas = []
        self._nome = nome
        self._id = id

    def get_mao(self) -> list:
        return self._cartas
    
    def get_id(self):
        return self._id

    def adicionar_cartas(self, cartas: list):
        for carta in cartas:
            self._cartas.append(carta)
    
    def remover_carta(self, carta_a_remover: object):
        if carta_a_remover in self._cartas:
            self._cartas.remove(carta_a_remover)

    def sem_cartas(self) -> bool:
        if len(self._cartas) == 0:
            return True
        else:
            return False

    def get_codigos_mao(self) -> list:  #Retorna uma lista com os códigos das cartas da mão do Jogador
        lista_codigos = []
        for carta in self._cartas:
            lista_codigos.append(carta.get_codigo())
        return lista_codigos
    
    def get_carta_por_nome_imagem(self, nome_imagem_carta: str) -> object:
        #formato esperado: "{rank}_of_{suit}"
        rank, suit = nome_imagem_carta.split("_of_")

        for carta in self._cartas:
            if carta.get_numero() == int(rank) and carta.get_naipe().name.lower() == suit.lower():
                return carta


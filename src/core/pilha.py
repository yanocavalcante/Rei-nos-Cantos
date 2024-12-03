class Pilha:
    def __init__(self, codigo_pilha):
        self._codigo_pilha = codigo_pilha
        self._cartas = []
    
    def get_codigo(self) -> str:
        return self._codigo_pilha

    def get_cartas(self) -> list:
        return self._cartas

    def verifica_colocacao_carta(self, carta) -> bool:
        if self._cartas == []:
            if self.verifica_canto():
                if carta.verificar_rei():
                    return True
                return False
            else:
                return True
        elif self._cartas[-1].get_numero() == carta.get_numero() + 1:
            if self._cartas[-1].verificar_cor_carta() != carta.verificar_cor_carta():
                return True
        return False

    def verifica_canto(self) -> bool:
        if self._codigo_pilha[0] == "C":
            return True

    def adicionar_cartas_pilha(self, carta_s):
        if type(carta_s) == list:
            for carta in carta_s:
                self._cartas.append(carta)
        else:
            self._cartas.append(carta_s)

    def retirar_cartas_pilha(self, carta_s):
        if type(carta_s) == list:
            for carta_a_retirar in carta_s:
                for carta in self._cartas:
                    if carta_a_retirar.get_codigo() == carta.get_codigo():
                        self._cartas.remove(carta)
        else:
            for carta in self._cartas:
                if carta_s.get_codigo() == carta.get_codigo():
                    self._cartas.remove(carta_s)
    
    def get_codigo_cartas(self) -> list: #Preciso dessa função para poder passar o código das cartas no JSON da req. HTTP
        lista_codigos = []
        for carta in self._cartas:
            lista_codigos.append(carta.get_codigo())
        return lista_codigos

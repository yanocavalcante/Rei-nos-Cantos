class Carta:
    def __init__(self, numero: int, naipe):
        self._numero = numero
        self._naipe = naipe
        self._codigo = self.gera_codigo()
    
    def get_numero(self) -> int:
        return self._numero

    def get_codigo(self) -> str:
        return self._codigo

    def get_naipe(self):
        return self._naipe

    def verificar_rei(self) -> bool:
        if self._numero != 13:
            return False
        else:
            return True

    def verificar_cor_carta(self) -> str:
        if self._naipe.value == 'Hearts' or self._naipe.value == 'Diamonds':
            return 'Vermelho'
        else:
            return "Preto"
    
    def gera_codigo(self):
        return self._naipe.name[0]+str(self._numero)


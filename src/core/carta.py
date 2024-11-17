class Carta:
    def __init__(self, numero: int, naipe):
        self._numero = numero
        self._naipe = naipe
        self.gera_codigo()

    def verificar_rei(self) -> bool:
        pass

    def verificar_cor_carta(self) -> str:
        pass

    def get_numero(self) -> int:
        return self._numero

    def get_codigo(self) -> str:
        return self._codigo
    
    def get_naipe(self):
        return self._naipe
    
    def gera_codigo(self):
        self._codigo = self._naipe.name[0]+str(self._numero)


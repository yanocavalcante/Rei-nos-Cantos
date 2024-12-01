from .pilha import Pilha
from .baralho import Baralho
import random


class Mesa:
    def __init__(self):
        print("Instanciou Mesa")
        cantos = []
        self._pilhas = [Pilha(str(i)) for i in range(4)]
        self._monte = Pilha("M")
        for i in range(4):
            codp = f"C{i}"
            canto = Pilha(codp)
            cantos.append(canto)
        self._pilhas.extend(cantos)

    def limpar_mesa(self):
        pass

    def comprar_carta_monte(self) -> object:
        return self._monte._cartas.pop(-1)

    def embaralhar_monte(self) -> list:
        cartas_do_baralho = self._baralho.get_cartas()
        random.shuffle(cartas_do_baralho)
        cartas_do_monte = cartas_do_baralho[:34]
        cartas_restantes = cartas_do_baralho[34:]
        for carta in cartas_do_monte:
            self._monte.adicionar_cartas_pilha([carta])
        return cartas_restantes

    def colocar_cartas_mesa(self, lista_cartas: list) -> list:
        count = 0
        for pilha in self._pilhas:
            if count == 4:
                return lista_cartas
            pilha.adicionar_cartas_pilha([lista_cartas.pop(0)])
            count += 1
    
    def instanciar_baralho(self):
        self._baralho = Baralho()

    def distribuir_cartas_jogador(self, lista_cartas: list, jogador) -> list:
        for i in range(7):
            jogador.adicionar_cartas([lista_cartas.pop(0)])
        return lista_cartas
    
    def get_monte(self) -> Pilha:
        return self._monte
    
    def get_pilhas(self) -> list:
        return self._pilhas
    
    def get_pilha_codigo(self, codp) -> Pilha:      #Retorna uma instância de pilha baseada no código fornecido
        if codp == "M":
            return self.get_monte()
        else:
            for pilha in self._pilhas:
                if pilha.get_codigo() == codp:
                    return pilha
    
    def get_baralho(self) -> list:
        return self._baralho

    def get_cartas_codigo(self, lista_codc) -> list:
        lista_cartas = []
        for codc in lista_codc:
            lista_cartas.append(self._baralho.get_carta_codigo(codc))
        return lista_cartas
    
    def get_pilha_por_direcao(self, direcao):
        if direcao == 'Norte':
            return self._pilhas[0]
        if direcao == 'Sul':
            return self._pilhas[1]
        if direcao == 'Leste':
            return self._pilhas[2]
        if direcao == 'Oeste':
            return self._pilhas[3]

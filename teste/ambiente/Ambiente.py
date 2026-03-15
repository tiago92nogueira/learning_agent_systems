from abc import ABC, abstractmethod

class Ambiente(ABC):

    def __init__(self, labirinto: list, agente_unico):
        self._labirinto = labirinto
        self._dimensoes = (len(labirinto), len(labirinto[0]))
        self._agente_unico = agente_unico
        self._pos_agente = self._encontrar_pos_inicial(labirinto)

        # método abstrato que cada ambiente implementa para instalar sensores
        self._configurar_sensores()

    #metodos auxiliares

    def _encontrar_pos_inicial(self, labirinto: list) -> tuple:
        for r in range(self._dimensoes[0]):
            for c in range(self._dimensoes[1]):
                if labirinto[r][c] == 'S':
                    return (r, c)
        return (0, 0)

    def _validar_movimento(self, r, c) -> bool:
        linhas, colunas = self._dimensoes
        if not (0 <= r < linhas and 0 <= c < colunas):
            return False
        if self._labirinto[r][c] == 1:
            return False
        return True

    

    def observacaoPara(self, agente) -> dict:
        return {
            'labirinto': self._labirinto,
            'pos_atual': self._pos_agente
        }

    def agir(self, accao: tuple | str, agente) -> bool:
        if accao == "FIM":
            print(f"Agente {agente} terminou a simulação.")
            return True
        
        if not isinstance(accao, tuple) or len(accao) != 2:
            return False

        r_nova, c_nova = accao

        if not self._validar_movimento(r_nova, c_nova):
            return False

        self._pos_agente = (r_nova, c_nova)
        return True

    

    @abstractmethod
    def _configurar_sensores(self):
        """Instala sensores próprios do ambiente."""
        pass

    @abstractmethod
    def atualizacao(self):
        """Reflete a dinâmica e a condição final do ambiente."""
        pass
from .Ambiente import Ambiente

class AmbienteLab(Ambiente):

    def __init__(self, labirinto: list, agente_unico, SensorDeProximidade):
        self._SensorClass = SensorDeProximidade
        super().__init__(labirinto, agente_unico)

    def _encontrar_pos_final(self, labirinto: list) -> tuple | None:
        for r in range(self._dimensoes[0]):
            for c in range(self._dimensoes[1]):
                if labirinto[r][c] == 'E':
                    return (r, c)
        return None

    def _configurar_sensores(self):
        self._pos_final = self._encontrar_pos_final(self._labirinto)

        if self._pos_final:
            sensor = self._SensorClass(self._pos_final)
            self._agente_unico.instala(sensor)

    def atualizacao(self):
        if self._pos_agente == self._pos_final:
            print("Agente atingiu o objetivo. Simulação concluída.")
            return True
        return False
from .Ambiente import Ambiente
class AmbienteFarol(Ambiente):

    def __init__(self, labirinto: list, agente_unico, SensorDeFarol):
        self._SensorClass = SensorDeFarol
        super().__init__(labirinto, agente_unico)

    def _encontrar_farol(self, labirinto: list) -> tuple | None:
        for r in range(self._dimensoes[0]):
            for c in range(self._dimensoes[1]):
                if labirinto[r][c] == 'F':
                    return (r, c)
        return None

    def _configurar_sensores(self):
        self._pos_farol = self._encontrar_farol(self._labirinto)

        if self._pos_farol:
            sensor = self._SensorClass(self._pos_farol)
            self._agente_unico.instala(sensor)

    def atualizacao(self):
        if self._pos_agente == self._pos_farol:
            print("Agente atingiu o Farol.")
            return True
        return False
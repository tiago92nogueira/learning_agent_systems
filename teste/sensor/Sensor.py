class Sensor:
    

    def __init__(self, pos_final: tuple):
        
        self._pos_final = pos_final

    def _distancia_manhattan(self, pos_atual: tuple) -> int:
        #calcula o menor numero de passos para chegar ao objetivo sem obstaculos
        r1, c1 = pos_atual
        r2, c2 = self._pos_final
       
        return abs(r1 - r2) + abs(c1 - c2)

    
    def calcular_prioridade(self, pos_vizinha: tuple, g_score_atual: int) -> float:
        f_score = self._distancia_manhattan(pos_vizinha)
        
        return f_score

    def __call__(self, pos_vizinha: tuple, g_score_atual: int) -> float:
        return self.calcular_prioridade(pos_vizinha, g_score_atual)
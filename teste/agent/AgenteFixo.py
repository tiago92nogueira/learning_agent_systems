class AgenteFixo:
    def __init__(self, pos_inicial: tuple):
        self.sensor = None
        self._labirinto = None
        self._pos_atual = pos_inicial
        self._movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self._visitados = {pos_inicial} 

    def instala(self, sensor):
        self.sensor = sensor

    def observacao(self, obs: dict):
        self._labirinto = obs.get('labirinto')
        nova_posicao = obs.get('pos_atual', self._pos_atual)
        
        if nova_posicao != self._pos_atual:
            self._visitados.add(nova_posicao)
            
        self._pos_atual = nova_posicao

    def age(self) -> tuple | str:
        if not self.sensor or not self._labirinto:
            return None

        r_atual, c_atual = self._pos_atual
        
        if (r_atual, c_atual) == self.sensor._pos_final:
            return "FIM"

        melhor_movimento = None
        melhor_prioridade = float('inf')

        for dr, dc in self._movimentos:
            r_viz, c_viz = r_atual + dr, c_atual + dc
            pos_viz = (r_viz, c_viz)

            if not (0 <= r_viz < len(self._labirinto) and 0 <= c_viz < len(self._labirinto[0])):
                continue
            if self._labirinto[r_viz][c_viz] == 1:
                continue
            
    
            prioridade = self.sensor.calcular_prioridade(pos_viz, 0)
            
            if prioridade < melhor_prioridade:
                melhor_prioridade = prioridade
                melhor_movimento = pos_viz
            
        return melhor_movimento
import numpy as np
from agent.Agent import Agent
from neural.NeuralNet import NeuralNet

class AgenteEvolutivo(Agent):
 
    INPUT_SIZE = 6 
    HIDDEN_SIZE = 16 
    OUTPUT_SIZE = 4
    
    def __init__(self, pos_inicial, lab_size=(9, 9), rede_neuronal=None):
        self.sensor = None
        self._labirinto = None
        self._pos_atual = pos_inicial
        self.lab_rows, self.lab_cols = lab_size 
        
        # config da rede
        if rede_neuronal:
            self.brain = rede_neuronal
        else:
            self.brain = NeuralNet(
                input_size=self.INPUT_SIZE, 
                hidden_size=self.HIDDEN_SIZE, 
                output_size=self.OUTPUT_SIZE
            )
            
        self._movimentos_mapa = [(-1, 0), (1, 0), (0, -1), (0, 1)] #direcoes
        
        # atributos para calculo de fitness
        self.passos_dados = 0
        self.posicoes_visitadas = set()
        self.posicoes_visitadas.add(pos_inicial)
        self.chegou_ao_fim = False
        self.bateu_na_parede = False

    @staticmethod
    def cria(nome_do_ficheiro_parametros: str):
        
        return AgenteEvolutivo((0,0))

    def instala(self, sensor):
        self.sensor = sensor

    def observacao(self, obs):
        self._labirinto = obs.get('labirinto')
        nova_pos = obs.get('pos_atual', self._pos_atual)
        
        # tam do lab
        if self._labirinto:
            self.lab_rows = len(self._labirinto)
            self.lab_cols = len(self._labirinto[0])

        if nova_pos != self._pos_atual:
            self._pos_atual = nova_pos
            if nova_pos not in self.posicoes_visitadas:
                self.posicoes_visitadas.add(nova_pos)
            self.passos_dados += 1

    def age(self):
        if not self.sensor or not self._labirinto:
            return None

        if self._pos_atual == self.sensor._pos_final:
            self.chegou_ao_fim = True
            return "FIM"
        inputs = []
        r, c = self._pos_atual
    
        for dr, dc in self._movimentos_mapa:
            r_viz, c_viz = r + dr, c + dc
            pos_viz = (r_viz, c_viz) 
            
            if not (0 <= r_viz < self.lab_rows and 0 <= c_viz < self.lab_cols) or \
            self._labirinto[r_viz][c_viz] == 1:
                val_input = -1.0 
            else:
                dist = self.sensor.calcular_prioridade(pos_viz, 0)
                max_dist = self.lab_rows + self.lab_cols
                val_input = 1.0 - (dist / max_dist)
                
                if pos_viz in self.posicoes_visitadas:
                    val_input -= 0.5

            inputs.append(val_input)

        inputs.append(r / (self.lab_rows - 1))
        inputs.append(c / (self.lab_cols - 1))

        output = self.brain.forward(inputs)
        indice_escolhido = np.argmax(output)
        movimento_escolhido = self._movimentos_mapa[indice_escolhido]
        
        return (r + movimento_escolhido[0], c + movimento_escolhido[1])

    def avaliacaoEstadoAtual(self, recompensa: float):
        pass
        
    def comunica(self, mensagem: str, de_agente):
        pass
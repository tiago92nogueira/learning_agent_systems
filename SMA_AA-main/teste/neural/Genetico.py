import numpy as np
import random
import copy
#e
class Genetico:
    def __init__(self, population_size, mutation_rate=0.05, elitism_count=2):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism_count = elitism_count

    def criar_nova_geracao(self, populacao_atual, fitness_scores):
        # ordena a pop pelo fitness
        sorted_indices = np.argsort(fitness_scores)[::-1]
        populacao_ordenada = [populacao_atual[i] for i in sorted_indices]
        
        nova_populacao = []
        
        # elitismo, o melhores ficam inalterados
        for i in range(self.elitism_count):
    # nova_populacao é uma lista vazia [], usamos append para adicionar o objeto
            nova_populacao.append(copy.deepcopy(populacao_ordenada[i]))
            
        #crossover e mutacao
        while len(nova_populacao) < self.population_size:
            pai1 = self._selecao_torneio(populacao_atual, fitness_scores)
            pai2 = self._selecao_torneio(populacao_atual, fitness_scores)
            
            filho = self._crossover(pai1, pai2)
            self._mutacao(filho)
            
            nova_populacao.append(filho)
            
        return nova_populacao

    def _selecao_torneio(self, populacao, fitness_scores, k=3):
        """Seleciona o melhor individuo de um grupo aleatorio de k individuos."""
        indices = np.random.choice(len(populacao), k)
        best_idx = indices[np.argmax([fitness_scores[i] for i in indices])]
        return populacao[best_idx]

    def _crossover(self, pai1, pai2):
        w1 = pai1.get_weights()
        w2 = pai2.get_weights()
        
        #ponto de corte aleatorio
        ponto_corte = random.randint(0, len(w1) - 1)
        
        novo_dna = np.concatenate((w1[:ponto_corte], w2[ponto_corte:]))
        
        #estrutura igual
        filho = copy.deepcopy(pai1)
        filho.set_weights(novo_dna)
        return filho

    def _mutacao(self, rede):
        weights = rede.get_weights()
        escala_mutacao = 0.1
        for i in range(len(weights)):
            if random.random() < self.mutation_rate:
                weights[i] += np.random.randn() * escala_mutacao
        rede.set_weights(weights)
        #test
import matplotlib.pyplot as plt

class GraficoFitness:
    def __init__(self):
        self.geracoes = []
        self.fitness_medio = []

    def adicionar(self, geracao, fitness_medio):
        self.geracoes.append(geracao)
        self.fitness_medio.append(fitness_medio)

    def mostrar(self):
        plt.figure()
        plt.plot(self.geracoes, self.fitness_medio)
        plt.xlabel("Geração")
        plt.ylabel("Fitness Médio")
        plt.title("Evolução do Fitness Médio")
        plt.grid(True)
        plt.show()

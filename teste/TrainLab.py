import json
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import copy

from neural.Genetico import Genetico
from neural.NeuralNet import NeuralNet
from agent.AgenteEvolutivo import AgenteEvolutivo
from ambiente.AmbienteLab import AmbienteLab
from sensor.Sensor import Sensor


def calcular_fitness(agente, sensor, colisoes, max_passos):
    casas_novas = len(agente.posicoes_visitadas)
    dist_ao_fim = sensor.calcular_prioridade(agente._pos_atual, 0)
    max_dist = agente.lab_rows + agente.lab_cols
    progresso = (max_dist - dist_ao_fim) / max_dist

    fitness = (casas_novas * 500) + (progresso * 100) - (colisoes * 20)

    if not agente.chegou_ao_fim and dist_ao_fim < 3:
        fitness *= 0.8

    if agente.chegou_ao_fim:
        return 200000 + (max_passos - agente.passos_dados) * 500

    return max(fitness, 1)


def encontrar_start_end(labirinto):
    start = (0, 0)
    end = (0, 0)
    lab_rows, lab_cols = len(labirinto), len(labirinto[0])
    for r in range(lab_rows):
        for c in range(lab_cols):
            if labirinto[r][c] == 'S':
                start = (r, c)
            elif labirinto[r][c] == 'E':
                end = (r, c)
    return start, end, (lab_rows, lab_cols)


def treinar(num_geracoes, tam_populacao):
    try:
        with open("parametros.json", 'r') as f:
            params = json.load(f)
    except FileNotFoundError:
        print("Erro: parametros.json não encontrado.")
        return

    labirinto = params['labirinto']
    start_pos, end_pos, lab_size = encontrar_start_end(labirinto)
    max_passos = params.get('max_passos', 200)

    genetico = Genetico(tam_populacao, mutation_rate=0.1, elitism_count=5)

    populacao = [NeuralNet(AgenteEvolutivo.INPUT_SIZE,
                           AgenteEvolutivo.HIDDEN_SIZE,
                           AgenteEvolutivo.OUTPUT_SIZE)
                 for _ in range(tam_populacao)]

    if os.path.exists("melhor_cerebro.json"):
        try:
            melhor_rede_anterior = NeuralNet.load_from_file("melhor_cerebro.json")
            if (melhor_rede_anterior.input_size == AgenteEvolutivo.INPUT_SIZE and
                melhor_rede_anterior.hidden_size == AgenteEvolutivo.HIDDEN_SIZE):
                num_elites = int(tam_populacao * 0.2)
                for j in range(num_elites):
                    populacao[j] = copy.deepcopy(melhor_rede_anterior)
                print(f"Rede carregada com sucesso em {num_elites} indivíduos.")
            else:
                print("Arquitetura incompatível detectada. Iniciando do zero.")
        except Exception as e:
            print(f"Erro ao carregar ficheiro: {e}")

    melhor_fitness_global = -float('inf')
    melhor_rede_global = None

    taxa_sucesso_por_geracao = []
    fitness_medio_por_geracao = []
    passos_medio_por_geracao = []
    heatmap = np.zeros(lab_size)

    print(f"Treino iniciado: {num_geracoes} gerações, População {tam_populacao}")

    for geracao in range(num_geracoes):
        fitnesses = []
        passos_da_geracao = []
        sucessos_nesta_geracao = 0 

        for cerebro in populacao:
            agente = AgenteEvolutivo(start_pos, lab_size=lab_size, rede_neuronal=cerebro)
            sensor = Sensor(end_pos)
            agente.instala(sensor)
            ambiente = AmbienteLab(labirinto, agente, Sensor)

            passos = 0
            colisoes = 0
            contador_estagnacao = 0
            terminou = False

            while passos < max_passos and not terminou:
                pos_anterior = agente._pos_atual

                obs = ambiente.observacaoPara(agente)
                agente.observacao(obs)
                acao = agente.age()

                if acao == "FIM" or acao is None:
                    terminou = True
                else:
                    movimento_valido = ambiente.agir(acao, agente)
                    if agente._pos_atual == pos_anterior:
                        contador_estagnacao += 1
                        if not movimento_valido:
                            colisoes += 1
                    else:
                        contador_estagnacao = 0

                if contador_estagnacao > 10:
                    terminou = True

                passos += 1

                pos = agente._pos_atual
                heatmap[pos[0], pos[1]] += 1

                if agente._pos_atual == end_pos:
                    agente.chegou_ao_fim = True
                    terminou = True

            if agente.chegou_ao_fim:
                sucessos_nesta_geracao += 1        

            fit = calcular_fitness(agente, sensor, colisoes, max_passos)
            fitnesses.append(fit)
            passos_da_geracao.append(passos)

            if fit > melhor_fitness_global:
                melhor_fitness_global = fit
                melhor_rede_global = copy.deepcopy(cerebro)
                print(f"New Record Gen {geracao+1}: Fit={fit:.1f} | Explorou={len(agente.posicoes_visitadas)} | Fim={agente.chegou_ao_fim}")

        percentagem_sucesso = (sucessos_nesta_geracao / tam_populacao) * 100
        taxa_sucesso_por_geracao.append(percentagem_sucesso)

        fitness_medio_por_geracao.append(np.mean(fitnesses))
        passos_medio_por_geracao.append(np.mean(passos_da_geracao))

        if (geracao + 1) % 10 == 0:
            print(f"Ger {geracao+1}: Média Fitness = {np.mean(fitnesses):.1f} | Média Passos = {np.mean(passos_da_geracao):.1f}")

        populacao = genetico.criar_nova_geracao(populacao, fitnesses)

    if melhor_rede_global:
        melhor_rede_global.save_to_file("melhor_cerebro.json")
        print("\nTreino Concluído. Melhor modelo guardado em 'melhor_cerebro.json'")

  
    plt.figure()
    plt.plot(range(1, num_geracoes + 1), fitness_medio_por_geracao)
    plt.xlabel("Geração")
    plt.ylabel("Fitness Médio")
    plt.title("Evolução do Fitness Médio")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(range(1, num_geracoes + 1), passos_medio_por_geracao)
    plt.xlabel("Geração")
    plt.ylabel("Passos Médios")
    plt.title("Evolução dos Passos por Geração")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar(label="Número de visitas")
    plt.title("Heatmap das posições mais visitadas")
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, num_geracoes + 1), taxa_sucesso_por_geracao, color='green', linewidth=2)
    plt.xlabel("Geração")
    plt.ylabel("Taxa de Sucesso (%)")
    plt.title("Percentagem da População que Atingiu o Objetivo")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.ylim(0, 105) 
    plt.show()


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
    treinar(num_geracoes=1000, tam_populacao=150)

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import numpy as np
from agent.AgenteEvolutivo import AgenteEvolutivo 
from ambiente.AmbienteFarol import AmbienteFarol 
from sensor.Sensor import Sensor
from neural.NeuralNet import NeuralNet
from Simulador import MotorDeSimulacao


class FarolEvo:
    """
    GUI para visualizar o Agente Evolutivo treinado no ambiente Farol ('F').
    """
    def __init__(self, master: tk.Tk, params_file="parametersFarol.json", brain_file="melhor_cerebroFarol.json"):
        self.master = master
        master.title("Visualização do Agente Evolutivo (Farol)")
        
        self.params_file = params_file
        self.brain_file = brain_file
        
        self.motor = None
        self.CELL_SIZE = 25 
        self.SPEED = 300 
        
        self.agente = None
        self.ambiente = None
        self.labirinto = None
        self.max_passos = 100
        self.auto_job = None
        self.agent_blob = None
        
        if self._load_simulation():
            self._setup_gui()
            self._update_display()
            self.master.after(1000, self._auto_run_step)

    def _find_start_pos(self, labirinto):
        """Encontra a posição 'S' no labirinto."""
        for r in range(len(labirinto)):
            for c in range(len(labirinto[0])):
                if labirinto[r][c] == 'S': return (r, c)
        return (0, 0)

    def _load_simulation(self):
        try:
            # Carregar Labirinto e Parâmetros
            if not os.path.exists(self.params_file):
                raise FileNotFoundError(f"Ficheiro '{self.params_file}' não encontrado.")
                
            with open(self.params_file, 'r') as f:
                params = json.load(f)
            self.labirinto = params['labirinto']
            self.max_passos = params.get('max_passos', 60)
            
            start_pos = self._find_start_pos(self.labirinto)
            
            # Calcular e passar lab_size 
            rows = len(self.labirinto)
            cols = len(self.labirinto[0])
            lab_size = (rows, cols)
           
            
            # Carregar Cérebro
            if not os.path.exists(self.brain_file):
                messagebox.showerror("Erro", f"Cérebro não encontrado: '{self.brain_file}'.\n\nPor favor, execute o 'TrainFarolEvo.py' primeiro!")
                self.master.destroy()
                return False
                
            print(f"A carregar rede neuronal de: {self.brain_file}")
            brain = NeuralNet.load_from_file(self.brain_file)
            
            # Criar Agente Evolutivo
            self.agente = AgenteEvolutivo(start_pos, lab_size=lab_size, rede_neuronal=brain) # Adicionado lab_size
            
            # Criar Ambiente
            self.ambiente = AmbienteFarol(self.labirinto, self.agente, Sensor)
            
            # Criar Motor de Simulação
            self.motor = MotorDeSimulacao(self.ambiente, self.agente)
            
            return True
            
        except Exception as e:
            messagebox.showerror("Erro Fatal (Simulação)", f"Ocorreu um erro ao inicializar a simulação.\n\nDetalhes: {e}\n\nVerifique:\n1. Ficheiro '{self.brain_file}' (se está vazio ou corrompido).\n2. Imports no '{os.path.basename(__file__)}' e em 'Simulador.py'.")
            self.master.destroy()
            return False

    def _setup_gui(self):
        """Desenha a interface e o labirinto estático"""
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        rows = len(self.labirinto)
        cols = len(self.labirinto[0])
        
        self.canvas = tk.Canvas(main_frame, width=cols*self.CELL_SIZE,
                                 height=rows*self.CELL_SIZE, bg="#e0e0e0")
        self.canvas.pack(pady=10)
        
        self.lbl_info = ttk.Label(main_frame, text="A carregar cérebro...", font=("Arial", 12))
        self.lbl_info.pack(pady=5)
        
        # Desenhar Labirinto
        for r in range(rows):
            for c in range(cols):
                x1, y1 = c*self.CELL_SIZE, r*self.CELL_SIZE
                x2, y2 = x1+self.CELL_SIZE, y1+self.CELL_SIZE
                cell = self.labirinto[r][c]
                
                color = "white"
                if cell == 1: color = "black"
                elif cell == 'S': color = "#aaffaa" # pos inicial
                elif cell == 'F': color = "#ffffaa" # farol
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#cccccc")

    def _update_display(self, status=""):
        if not self.motor: return
        
        if self.agent_blob:
            self.canvas.delete(self.agent_blob)
            
        pos = self.ambiente._pos_agente
        r, c = pos
        
        x1, y1 = c*self.CELL_SIZE + 5, r*self.CELL_SIZE + 5
        x2, y2 = x1 + self.CELL_SIZE - 10, y1 + self.CELL_SIZE - 10
        self.agent_blob = self.canvas.create_oval(x1, y1, x2, y2, fill="purple", outline="white", width=2)
        
        text = f"Passo: {self.motor._passo_atual}/{self.max_passos}"
        if status: text += f" | {status}"
        self.lbl_info.config(text=text)
        self.master.update_idletasks()

    def _auto_run_step(self):
        terminou = self.motor.executa(max_passos=self.max_passos)
        
        if terminou:
            if getattr(self.agente, 'chegou_ao_fim', False):
                self._update_display("SUCESSO! Farol Alcançado! :)")
            else:
                self._update_display("FIM: Limite ou Bloqueio :(")
            return

        self._update_display()
        self.auto_job = self.master.after(self.SPEED, self._auto_run_step)

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)

    root = tk.Tk()
    app = FarolEvo(root) 
    root.mainloop()
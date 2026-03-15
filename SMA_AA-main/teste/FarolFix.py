
import tkinter as tk
from tkinter import ttk, messagebox
import json

from Simulador import MotorDeSimulacao

class FarolFix:

    def __init__(self, master: tk.Tk, params_file: str = "parametros_farol.json"):
        self.master = master
        master.title("Simulação Automática do Agente no Farol")

        self.params_file = params_file
        self.motor: MotorDeSimulacao = None
        self.labirinto_display = [] 

        self.CELL_SIZE = 40
        self.SPEED = 800  

        self.agente = None
        self.ambiente = None
        self.labirinto = None
        self.max_passos = 100
        self.auto_job = None 

        if self._load_simulation():
            self._setup_gui()
            self._update_display()
            self.master.after(500, self._auto_run_step)

    def _load_simulation(self):
        """Cria MotorDeSimulacao e inicializa variáveis."""
        try:
            self.motor = MotorDeSimulacao.cria(self.params_file)
            if not self.motor:
                messagebox.showerror("Erro", "Nao foi possivel criar o motor de simulacao.")
                self.master.destroy()
                return False

            self.agente = self.motor.listaAgentes()[0]
            self.ambiente = self.motor._ambiente
            self.labirinto = self.ambiente._labirinto

            with open(self.params_file, 'r') as f:
                params = json.load(f)
            self.max_passos = params.get("max_passos", 100)
            return True

        except Exception as e:
            messagebox.showerror("Erro de Inicialização", f"Ocorreu um erro: {e}")
            self.master.destroy()
            return False

    def _setup_gui(self):
        """Configura canvas e labels da GUI."""
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        rows, cols = len(self.labirinto), len(self.labirinto[0])
        self.canvas = tk.Canvas(main_frame, width=cols*self.CELL_SIZE,
                                 height=rows*self.CELL_SIZE, bg="lightgray", borderwidth=2, relief="groove")
        self.canvas.pack(pady=10)

        self.step_label = ttk.Label(main_frame, text="Iniciando...", font=('Helvetica', 12, 'bold'))
        self.step_label.pack(pady=5)

        # Desenhar labirinto
        for r in range(rows):
            row_display = []
            for c in range(cols):
                x1, y1 = c*self.CELL_SIZE, r*self.CELL_SIZE
                x2, y2 = x1+self.CELL_SIZE, y1+self.CELL_SIZE
                cell = self.labirinto[r][c]
                color = "white"
                if cell == 1: color = "black"
                elif cell == "S": color = "green"
                elif cell == "F": color = "yellow" 
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                row_display.append(rect)
            self.labirinto_display.append(row_display)

        self.agent_rect = None

    def _update_display(self, message=""):
        """Atualiza a posição do agente e status na GUI."""
        if not self.motor: return

        if self.agent_rect:
            self.canvas.delete(self.agent_rect)

        # Usamos _pos_agente do ambiente
        pos = self.ambiente._pos_agente 
        
        if pos:
            r, c = pos
            x1, y1 = c*self.CELL_SIZE, r*self.CELL_SIZE
            x2, y2 = x1+self.CELL_SIZE, y1+self.CELL_SIZE
            self.agent_rect = self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="blue", outline="darkblue")

        text = f"Passo: {self.motor._passo_atual}"
        if message:
            text += f" | {message}"
        self.step_label.config(text=text)
        self.master.update_idletasks()

    def _auto_run_step(self):
        """Executa um passo da simulação e agenda o próximo."""
        if self.motor._simulacao_terminada:
            return

        terminou = self.motor.executa(max_passos=self.max_passos)

        if terminou:
            # Verifica se o Farol foi atingido
            if self.ambiente._pos_agente == self.ambiente._pos_farol:
                status = "Farol Alcançado!"
            else:
                status = "Limite de Passos Atingido ou Bloqueio."
            self._update_display(status)
            return

        self._update_display(f"A mover para {self.ambiente._pos_agente}")
        self.auto_job = self.master.after(self.SPEED, self._auto_run_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = FarolFix(root, "parametersFarol.json")
    root.mainloop()
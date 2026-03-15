
import json
import time 


from agent.AgenteFixo import AgenteFixo 
from ambiente.AmbienteLab import AmbienteLab
from ambiente.AmbienteFarol import AmbienteFarol
from sensor.Sensor import Sensor 

class MotorDeSimulacao:
    

    def __init__(self, ambiente, agente):
        self._ambiente = ambiente
        self._agente_unico = agente
        self._passo_atual = 0
        self._simulacao_terminada = False
        
        
        self._simbolo_objetivo = 'F' if isinstance(ambiente, AmbienteFarol) else 'E'


    @staticmethod
    def _encontrar_pos_inicial(labirinto: list) -> tuple:
        dimensoes = (len(labirinto), len(labirinto[0]))
        for r in range(dimensoes[0]):
            for c in range(dimensoes[1]):
                if labirinto[r][c] == 'S':
                    return (r, c)
        return (0, 0)
    
    @staticmethod
    def _verificar_objetivo(labirinto: list) -> str | None:
        """Verifica se o objetivo é 'E' (Labirinto) ou 'F' (Farol)."""
        for r in labirinto:
            if 'F' in r:
                return 'FAROL'
            if 'E' in r:
                return 'LABIRINTO'
        return None


    @staticmethod
    def cria(nome_do_ficheiro_parametros: str) -> "MotorDeSimulacao":
        try:
            with open(nome_do_ficheiro_parametros, 'r') as f:
                parametros = json.load(f)
        except Exception as e:
            print(f"Erro ao ler ficheiro: {e}")
            return None

        labirinto_matriz = parametros.get('labirinto', [])
        pos_inicial_agente = MotorDeSimulacao._encontrar_pos_inicial(labirinto_matriz)
        
        tipo_ambiente = MotorDeSimulacao._verificar_objetivo(labirinto_matriz)
        
        agente = AgenteFixo(pos_inicial=pos_inicial_agente)

        if tipo_ambiente == 'FAROL':
            print("criar ambiente Farol (F)")
            
            ambiente = AmbienteFarol(
                labirinto=labirinto_matriz,
                agente_unico=agente,
                SensorDeFarol=Sensor 
            )
        elif tipo_ambiente == 'LABIRINTO':
            print("criar ambiente Labirinto (E)")
            
            ambiente = AmbienteLab(
                labirinto=labirinto_matriz,
                agente_unico=agente,
                SensorDeProximidade=Sensor 
            )
        else:
            print(" Erro: Não foi encontrado E nem F no labirinto.")
            return None

        return MotorDeSimulacao(ambiente, agente)

    def listaAgentes(self) -> list:
        return [self._agente_unico]

    def executa(self, max_passos: int = 100) -> bool: #executa apenas um passo da simulacao
      
        if self._simulacao_terminada:
            return True
            
        if self._passo_atual >= max_passos:
            self._simulacao_terminada = True
            return True

        
        self._passo_atual += 1
        print(f"\n[PASSO {self._passo_atual}]")
        
        obs = self._ambiente.observacaoPara(self._agente_unico)
        self._agente_unico.observacao(obs)
        
        acao = self._agente_unico.age()
        
        if acao == "FIM":
            print(f"Objetivo ('{self._simbolo_objetivo}') alcançado em {self._passo_atual} movimentos.")
            self._simulacao_terminada = True
            return True
        
        if acao is None:
            print("Agente bloqueado.")
            self._simulacao_terminada = True
            return True
        
        movimento_valido = self._ambiente.agir(acao, self._agente_unico)
        
        if not movimento_valido:
            print(f"Ação inválida (colisão).")
        else:
            print(f"Agente moveu-se.")
        
        return False
        #s
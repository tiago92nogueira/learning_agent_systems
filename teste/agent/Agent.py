from abc import ABC, abstractmethod


class Agent(ABC):

    @staticmethod
    @abstractmethod
    def cria(nome_do_ficheiro_parametros: str):
        """Cria um agente usando configurações lidas de um ficheiro."""
        pass

    @abstractmethod
    def observacao(self, obs):
        """Recebe uma observação fornecida pelo ambiente."""
        pass

    @abstractmethod
    def age(self):
        """Gera a ação que o agente pretende realizar."""
        pass

    @abstractmethod
    def avaliacaoEstadoAtual(self, recompensa: float):
        """Recebe feedback de desempenho (recompensa)."""
        pass

    @abstractmethod
    def instala(self, sensor):
        """Instala um sensor no agente."""
        pass



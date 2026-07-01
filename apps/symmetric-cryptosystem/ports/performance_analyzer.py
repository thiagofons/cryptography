from abc import ABC, abstractmethod
from typing import Any, Callable, Tuple


class PerformanceAnalyzerPort(ABC):
    """
    Porta de saída (Outbound Port) que define a interface para 
    análise de desempenho de blocos de código.
    """

    @abstractmethod
    def measure_execution(self, func: Callable[[], Any]) -> Tuple[Any, float]:
        """
        Executa um bloco de código (via Callable) e calcula o tempo decorrido.

        :param func: Uma função ou expressão lambda sem argumentos que encapsula a lógica a ser medida.
        :return: Uma tupla contendo (resultado_da_execucao, tempo_em_segundos).
        """
        pass
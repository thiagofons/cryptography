import time
from typing import Any, Callable, Tuple

from ports import PerformanceAnalyzerPort


class TimePerformanceAnalyzerAdapter(PerformanceAnalyzerPort):
    """
    Adaptador que implementa a medição de performance baseada em tempo de CPU/Relógio.
    Utiliza o perf_counter() para garantir precisão de nanossegundos.
    """

    def measure_execution(self, func: Callable[[], Any]) -> Tuple[Any, float]:
        """
        Garante a medição isolada e precisa da função passada por parâmetro.
        """
        # Captura o tempo imediatamente antes da execução
        start_time = time.perf_counter()
        
        # Executa a operação criptográfica (Cifração ou Decifração)
        result = func()
        
        # Captura o tempo imediatamente após a execução
        end_time = time.perf_counter()
        
        # Calcula a diferença
        elapsed_time = end_time - start_time
        
        return result, elapsed_time
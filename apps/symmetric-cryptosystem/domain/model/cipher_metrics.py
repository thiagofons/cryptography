from dataclasses import dataclass, field
from typing import List


@dataclass
class CipherMetrics:
    """Estrutura de dados para armazenar as métricas de um algoritmo específico."""
    name: str
    encryption_times: List[float] = field(default_factory=list)
    decryption_times: List[float] = field(default_factory=list)
    is_correct: bool = True
from abc import ABC, abstractmethod


class ComparisonReportPort(ABC):
    @abstractmethod
    def generate(self, original_cipher_metrics: dict, aes_metrics: dict) -> None:
        """Gera e renderiza o relatório comparativo baseado nas métricas recebidas."""
        pass
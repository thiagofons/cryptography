from abc import ABC, abstractmethod


class TerminalPrinterPort(ABC):
    @abstractmethod
    def print_title(self, text: str) -> None:
        """Exibe um cabeçalho ou título de destaque na tela."""
        pass

    @abstractmethod
    def print_step(self, label: str, value: str) -> None:
        """Exibe uma linha de informação no formato 'Etapa: Valor'."""
        pass

    @abstractmethod
    def print_alert(self, text: str) -> None:
        """Exibe uma informação importante ou de destaque secundário."""
        pass
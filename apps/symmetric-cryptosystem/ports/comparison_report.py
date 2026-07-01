# Em: ports/comparison_report_port.py
from abc import ABC, abstractmethod
from typing import Dict, List


class ComparisonReportPort(ABC):
    """
    Porta de saída (Outbound Port) que define o contrato para 
    geração, acúmulo de métricas e exibição de relatórios comparativos.
    """

    @abstractmethod
    def add_results(
        self, 
        name: str, 
        metadata: Dict[str, str], 
        enc_times: List[float], 
        dec_times: List[float], 
        memory_bytes: float
    ) -> None:
        """
        Adiciona os resultados dinâmicos e metadados estáticos de um 
        criptossistema específico para o acumulador do relatório.

        :param name: Nome identificador do algoritmo (ex: 'AES (Padrão de Mercado)').
        :param metadata: Dicionário contendo as propriedades teóricas vindas do CipherPort.
        :param enc_times: Lista com os tempos de cada rodada de cifração.
        :param dec_times: Lista com os tempos de cada rodada de decifração.
        :param memory_bytes: Pico de consumo de memória RAM coletado em bytes.
        """
        pass

    @abstractmethod
    def print_summary(self) -> None:
        """
        Processa todos os dados acumulados e renderiza o sumário final 
        formatado (neste caso, em estrutura de tabela) para o destino configurado.
        """
        pass
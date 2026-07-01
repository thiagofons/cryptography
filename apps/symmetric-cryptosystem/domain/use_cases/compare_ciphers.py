from typing import List

from domain.model import CipherMetrics, ComparisonReport
from ports import CipherPort, PerformanceAnalyzerPort, TerminalPrinterPort


class CompareCiphersUseCase:
    def __init__(self, first_cipher: CipherPort, second_cipher: CipherPort, analyser: PerformanceAnalyzerPort, printer: TerminalPrinterPort):
        self._first_cipher = first_cipher
        self._second_cipher = second_cipher
        self._analyser = analyser
        self._printer = printer

    def execute(self, data_inputs: List[bytes], key: bytes) -> ComparisonReport:
        """
        Orquestra a execução dos testes de estresse, coleta métricas e valida a corretude.
        """
        report = ComparisonReport()
        
        # Lista dos ciphers que vamos testar dinamicamente
        ciphers_to_test = [
            (self._first_cipher.__class__.__name__, self._first_cipher),
            (self._second_cipher.__class__.__name__, self._second_cipher)
        ]

        for name, cipher in ciphers_to_test:
            metrics = CipherMetrics(name=name)
            
            for data in data_inputs:
                # 1. Medição do processo de Cifração
                # O analyzer recebe uma função lambda para medir a execução isoladamente
                ciphertext, enc_time = self._analyzer.measure_execution(
                    lambda: cipher.encrypt(data, key)
                )
                metrics.encryption_times.append(enc_time)

                # 2. Medição do processo de Decifração
                decrypted_data, dec_time = self._analyzer.measure_execution(
                    lambda: cipher.decrypt(ciphertext, key)
                )
                metrics.decryption_times.append(dec_time)

                # 3. Análise de Segurança/Corretude Básica
                # Se o dado decifrado não for idêntico ao original, o algoritmo falhou
                if decrypted_data != data:
                    metrics.is_correct = False

            # Adiciona os resultados coletados ao relatório final
            report.add_metric(cipher_name=name, metrics=metrics)

        return report
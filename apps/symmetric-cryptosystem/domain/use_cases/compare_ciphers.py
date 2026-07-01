from typing import List

from domain.model import CipherMetrics
from ports import CipherPort, ComparisonReportPort, PerformanceAnalyzerPort


class CompareCiphersUseCase:
    def __init__(
        self, 
        first_cipher: CipherPort, 
        second_cipher: CipherPort, 
        analyzer: PerformanceAnalyzerPort, 
        report_service: ComparisonReportPort 
    ):
        self._first_cipher = first_cipher
        self._second_cipher = second_cipher
        self._analyzer = analyzer
        self._report_service = report_service  

    def execute(self, data_inputs: List[bytes], key: bytes) -> None:
        """
        Orquestra a execução dos testes de estresse, coleta métricas, 
        valida a corretude e dispara a geração do relatório.
        """        
        ciphers_to_test = [
            (self._first_cipher.__class__.__name__, self._first_cipher),
            (self._second_cipher.__class__.__name__, self._second_cipher)
        ]

        collected_results = {}

        for name, cipher in ciphers_to_test:
            metrics = CipherMetrics(name=name)
            
            for data in data_inputs:
                ciphertext, enc_time = self._analyzer.measure_execution(
                    lambda: cipher.encrypt(data, key)
                )
                metrics.encryption_times.append(enc_time)

                decrypted_data, dec_time = self._analyzer.measure_execution(
                    lambda: cipher.decrypt(ciphertext, key)
                )
                metrics.decryption_times.append(dec_time)

                if decrypted_data != data:
                    metrics.is_correct = False

            collected_results[name] = metrics

        first_name = self._first_cipher.__class__.__name__
        second_name = self._second_cipher.__class__.__name__
        
        self._report_service.generate(
            original_cipher_metrics=collected_results.get(first_name),
            aes_metrics=collected_results.get(second_name)
        )
import tracemalloc
from typing import List

from ports import CipherPort, ComparisonReportPort, PerformanceAnalyzerPort


class CompareCiphersUseCase:
    def __init__(
        self, 
        first_cipher: CipherPort, 
        second_cipher: CipherPort, 
        analyzer: PerformanceAnalyzerPort,
        report_service: ComparisonReportPort
    ) -> None:
        self._first_cipher = first_cipher
        self._second_cipher = second_cipher
        self._analyzer = analyzer
        self._report_service = report_service  # Armazena o adapter de relatório injetado

    def execute(self, data_inputs: List[bytes], key: bytes) -> None:
        ciphers_to_test = [
            ("Seu Criptossistema Original", self._first_cipher),
            ("AES (Padrão de Mercado)", self._second_cipher)
        ]

        for name, cipher in ciphers_to_test:
            enc_times = []
            dec_times = []
            
            tracemalloc.start()
            
            for data in data_inputs:
                # Medição de Cifração
                ciphertext, enc_time = self._analyzer.measure_execution(lambda: cipher.encrypt(data, key))
                enc_times.append(enc_time)

                # Medição de Decifração
                _, dec_time = self._analyzer.measure_execution(lambda: cipher.decrypt(ciphertext, key))
                dec_times.append(dec_time)
                
            _, memory_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            # Alimenta o serviço de relatório que foi injetado pela MAIN
            self._report_service.add_results(
                name=name, 
                metadata=cipher.metadata, 
                enc_times=enc_times, 
                dec_times=dec_times, 
                memory_bytes=memory_peak
            )

        # Dispara a impressão utilizando o adapter que a Main escolheu
        self._report_service.print_summary()
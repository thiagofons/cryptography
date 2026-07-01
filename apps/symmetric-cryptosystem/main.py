import sys
from typing import List

from adapters import (AesCipherAdapter, CustomCipherAdapter,
                      RichTerminalPrinterAdapter,
                      TimePerformanceAnalyzerAdapter)
from domain.use_cases import CompareCiphersUseCase
from ports import CipherPort, PerformanceAnalyzerPort, TerminalPrinterPort


def main ():
    # Instances
    printer: TerminalPrinterPort = RichTerminalPrinterAdapter()

    custom_cipher: CipherPort = CustomCipherAdapter()
    aes_cipher: CipherPort = AesCipherAdapter()
    
    analyzer: PerformanceAnalyzerPort = TimePerformanceAnalyzerAdapter()

    # Use case
    comparison_use_case = CompareCiphersUseCase(
        first_cipher=custom_cipher,
        second_cipher=aes_cipher,
        analyzer=analyzer,
        printer=printer        
    )

    # Input data
    test_texts: List[bytes] = [
        b"Mensagem curta",
        b"Uma mensagem consideravelmente mais longa para testar o comportamento dos blocos.",
        b"A" * 1024 * 1024  # 1MB
    ]

    master_key: bytes = b"ChaveSecreta32BytesOriginalAES!"

    # ===========================
    # Execution
    # ===========================
    try:
        printer.print_title("Starting analysis")
        report = comparison_use_case.execute(data_inputs=test_texts, key=master_key)

        report.print_summary()

    except Exception as e:
        printer.print_alert(f"Error: critical failure executing the test\n\n{e}")
        sys.exit(1)

    return

if __name__ == "__main__":
    main()
from typing import Dict

from domain.model import CipherMetrics


class ComparisonReport:
    """Objeto de valor que consolida os resultados obtidos pelo Caso de Uso."""
    def __init__(self):
        self.results: Dict[str, CipherMetrics] = {}

    def add_metric(self, cipher_name: str, metrics: CipherMetrics):
        self.results[cipher_name] = metrics

    def print_summary(self) -> None:
        print("\n" + "="*40)
        print("      RELATÓRIO DE PERFORMANCE      ")
        print("="*40)
        for name, metrics in self.results.items():
            avg_enc = sum(metrics.encryption_times) / len(metrics.encryption_times)
            avg_dec = sum(metrics.decryption_times) / len(metrics.decryption_times)
            status = "✓ Sucesso" if metrics.is_correct else "❌ Falha na Decifração"
            
            print(f"\nCriptossistema: {name}")
            print(f"  Integridade dos dados: {status}")
            print(f"  Tempo Médio de Cifração:   {avg_enc:.6f} segundos")
            print(f"  Tempo Médio de Decifração: {avg_dec:.6f} segundos")
        print("="*40)
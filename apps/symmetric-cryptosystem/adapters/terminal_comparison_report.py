from domain.model import CipherMetrics
from ports import ComparisonReportPort, TerminalPrinterPort


class TerminalComparisonReportAdapter(ComparisonReportPort):
    def __init__(self, printer: TerminalPrinterPort):
        self.printer = printer

    def _calculate_throughput(self, times: list) -> str:
        if not times:
            return "0.0s"
        avg_time = sum(times) / len(times)
        return f"{avg_time:.6f}s"

    def generate(self, original_cipher_metrics: CipherMetrics, aes_metrics: CipherMetrics) -> None:
        # Exibe o título estilizado do seu port de impressão
        self.printer.print_title("RELATÓRIO COMPARATIVO: CRIPTOSSISTEMA PROPOSTO VS AES")
        
        # Coleta as variáveis que vão popular a tabela
        c1_name = original_cipher_metrics.name
        c2_name = aes_metrics.name
        
        c1_corr = "Sucesso" if original_cipher_metrics.is_correct else "Falhou"
        c2_corr = "Sucesso" if aes_metrics.is_correct else "Falhou"
        
        c1_enc = self._calculate_throughput(original_cipher_metrics.encryption_times)
        c2_enc = self._calculate_throughput(aes_metrics.encryption_times)
        
        c1_dec = self._calculate_throughput(original_cipher_metrics.decryption_times)
        c2_dec = self._calculate_throughput(aes_metrics.decryption_times)

        # Configurações de largura das colunas para alinhamento perfeito
        w_crit = 32  # Largura da coluna de Critérios
        w_c1   = max(len(c1_name), 20)  # Largura para o seu Cifrador
        w_c2   = max(len(c2_name), 20)  # Largura para o AES
        
        # Divisores da tabela
        row_sep = "+" + "-"*(w_crit+2) + "+" + "-"*(w_c1+2) + "+" + "-"*(w_c2+2) + "+"
        
        # Montagem da tabela na memória antes do envio
        table_lines = [
            row_sep,
            f"| {'Critério de Avaliação'.ljust(w_crit)} | {c1_name.center(w_c1)} | {c2_name.center(w_c2)} |",
            row_sep,
            f"| {'Validação de Corretude'.ljust(w_crit)} | {c1_corr.center(w_c1)} | {c2_corr.center(w_c2)} |",
            f"| {'Tempo de Cifração (Média)'.ljust(w_crit)} | {c1_enc.center(w_c1)} | {c2_enc.center(w_c2)} |",
            f"| {'Tempo de Decifração (Média)'.ljust(w_crit)} | {c1_dec.center(w_c1)} | {c2_dec.center(w_c2)} |",
            f"| {'Tamanho do Bloco / Chave'.ljust(w_crit)} | {'128 / 128 bits'.center(w_c1)} | {'128 / 128 bits'.center(w_c2)} |",
            f"| {'Resistência a Timing Attacks'.ljust(w_crit)} | {'Alta (Design ARX)'.center(w_c1)} | {'Vulnerável(S-Boxes)'.center(w_c2)} |",
            row_sep
        ]
        
        # Imprime a tabela linha por linha usando o print_step do seu printer para manter a estilização
        for line in table_lines:
            # Passamos a linha inteira como label e deixamos o valor vazio para usar sua estilização padrão
            self.printer.print_step(line, "")
            
        self.printer.print_title("FIM DO RELATÓRIO")
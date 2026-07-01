import textwrap

from ports import ComparisonReportPort, TerminalPrinterPort


class TerminalComparisonReportAdapter(ComparisonReportPort):
    """
    Adaptador que formata os dados do relatório utilizando os métodos
    semânticos do TerminalPrinterPort em formato de tabela.
    """
    
    def __init__(self, printer: TerminalPrinterPort):
        self._printer = printer
        self.dynamic_metrics = {}
        self.static_metadata = {}

    def add_results(self, name: str, metadata: dict, enc_times: list, dec_times: list, memory_bytes: float):
        avg_enc_time = sum(enc_times) / len(enc_times) if enc_times else 0.001
        
        self.dynamic_metrics[name] = {
            "avg_time": avg_enc_time,
            "memory": memory_bytes / 1024  # Converte para KB
        }
        self.static_metadata[name] = metadata

    def print_summary(self) -> None:
        aes = "AES (Padrão de Mercado)"
        lince = "Seu Criptossistema Original"
        
        m_aes = self.static_metadata.get(aes, {})
        m_lince = self.static_metadata.get(lince, {})
        d_aes = self.dynamic_metrics.get(aes, {"avg_time": 0, "memory": 0})
        d_lince = self.dynamic_metrics.get(lince, {"avg_time": 0, "memory": 0})

        self._printer.print_title("RELATÓRIO COMPARATIVO")
        
        border = "=" * 100
        separator = "-" * 100
        
        self._printer.print_alert(border)
        header_row = f"{'PROPRIEDADE':<26} | {'AES (PADRÃO DE MERCADO)':<33} | {'LINCE-ARX (AUTORAL)':<33}"
        self._printer.print_alert(header_row)
        self._printer.print_alert(border)

        def _render_multi_line_row(prop_name: str, aes_val: str, lince_val: str):
            aes_lines = textwrap.wrap(aes_val, width=33) if aes_val else ["N/A"]
            lince_lines = textwrap.wrap(lince_val, width=33) if lince_val else ["N/A"]
            
            max_lines = max(len(aes_lines), len(lince_lines))
            
            for i in range(max_lines):
                p_chunk = prop_name if i == 0 else ""
                a_chunk = aes_lines[i] if i < len(aes_lines) else ""
                l_chunk = lince_lines[i] if i < len(lince_lines) else ""
                
                row_text = f"{p_chunk:<26} | {a_chunk:<33} | {l_chunk:<33}"
                self._printer.print_step(row_text, "")
            
            # Adiciona um espaço em branco logo após a linha terminar para dar o "respiro"
            self._printer.print_step("", "")

        # 2. Propriedades Estruturais
        _render_multi_line_row("Tamanho de Chave", m_aes.get('key_size', 'N/A'), m_lince.get('key_size', 'N/A'))
        _render_multi_line_row("Tamanho de Bloco", m_aes.get('block_size', 'N/A'), m_lince.get('block_size', 'N/A'))
        
        # 3. Métricas de Desempenho (Dinâmicas)
        _render_multi_line_row("Velocidade (Tempo Médio)", f"{d_aes.get('avg_time'):.6f} s", f"{d_lince.get('avg_time'):.6f} s")
        _render_multi_line_row("Consumo de Memória", f"{d_aes.get('memory'):.2f} KB", f"{d_lince.get('memory'):.2f} KB")

        # 4. Propriedades Arquiteturais e Segurança
        _render_multi_line_row("Paralelização", m_aes.get('parallelization', 'N/A'), m_lince.get('parallelization', 'N/A'))
        _render_multi_line_row("Difusão e Confusão", "S-Boxes / MixColumns", "Operações ARX Iterativas")
        _render_multi_line_row("Resistência a Ataques", m_aes.get('attack_resistance', 'N/A'), m_lince.get('attack_resistance', 'N/A'))
        _render_multi_line_row("Simplicidade Impl.", m_aes.get('implementation_simplicity', 'N/A'), m_lince.get('implementation_simplicity', 'N/A'))
        _render_multi_line_row("Escalabilidade", m_aes.get('scalability', 'N/A'), m_lince.get('scalability', 'N/A'))
        
        self._printer.print_alert(border)
        self._printer.print_title("FIM DO RELATÓRIO")
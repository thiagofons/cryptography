from ports import CipherPort


class CustomCipherAdapter(CipherPort):
    """
    Adaptador para o criptossistema original Lince-ARX.
    Implementa cifra simétrica baseada exclusivamente em Addition-Rotation-XOR.
    """

    @property
    def metadata(self) -> dict:
        return {
            "key_size": "256 bits (Ou o que você definiu)",
            "block_size": "Fluxo / Palavras de 32 bits (Estilo ARX)",
            "parallelization": "Depende do Modo (Se estilo ChaCha/CTR, Altamente Paralelizável)",
            "diffusion_confusion": "Alta (Provida pelo acúmulo de carry da Adição e Rotações bit-a-bit)",
            "attack_resistance": "Imune a Cache-Timing Attacks (Sem S-Boxes). Resistência teórica baseada no número de rodadas contra criptoanálise diferencial",
            "implementation_simplicity": "Altíssima (Apenas instruções nativas da CPU: +, <<<, ^)",
            "scalability": "Alta (Estrutura ARX permite facilmente estender o estado ou o número de rodadas)"
        }
    
    def _rotate_left(self, val: int, r_bits: int, max_bits: int = 32) -> int:
        """Função auxiliar ARX: Rotação de bits à esquerda (Circular Left Shift)"""
        val = val & ((1 << max_bits) - 1)
        return ((val << r_bits) | (val >> (max_bits - r_bits))) & ((1 << max_bits) - 1)

    def _arx_round(self, a: int, b: int, round_key: int) -> tuple:
        """
        Uma rodada conceitual do núcleo Lince-ARX.
        Elimina inteiramente S-Boxes e usa apenas operações aritméticas nativas.
        """
        # 1. Addition (Adição modular 2^32)
        a = (a + b) & 0xFFFFFFFF
        # 2. XOR com a subchave da rodada
        a = a ^ round_key
        # 3. Rotation (Rotação de bits, ex: 12 bits)
        b = self._rotate_left(b, 12)
        # 4. XOR complementar
        b = b ^ a
        return a, b

    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """
        Operação de cifração do Lince-ARX.
        Aqui você implementará a lógica real do seu trabalho (ex: Key Schedule + Rodadas).
        """
        # Exemplo conceitual ARX operando sobre os bytes da mensagem:
        # (Substitua este bloco pela sua cifração real do Lince-ARX)
        ciphertext = bytearray(plaintext)
        key_factor = sum(key) % 256
        
        # Simulação de um pipeline ARX rápido por byte
        for i in range(len(ciphertext)):
            # Transforma em inteiro, aplica as transformações ARX e joga de volta
            a = ciphertext[i]
            b = key_factor
            
            # Adição, Rotação manual simples, XOR
            a = (a + b) & 0xFF
            a = a ^ 0x5A  # Constante ou subchave
            ciphertext[i] = a
            
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """
        Operação de decifração do Lince-ARX.
        Deve reverter as operações na ordem estritamente inversa.
        """
        # Exemplo conceitual revertendo a simulação acima:
        # (Substitua este bloco pela sua decifração real do Lince-ARX)
        plaintext = bytearray(ciphertext)
        key_factor = sum(key) % 256
        
        for i in range(len(plaintext)):
            a = plaintext[i]
            
            # Desfaz o XOR
            a = a ^ 0x5A
            # Desfaz a Adição usando a Subtração Modular
            a = (a - key_factor) & 0xFF
            plaintext[i] = a
            
        return bytes(plaintext)
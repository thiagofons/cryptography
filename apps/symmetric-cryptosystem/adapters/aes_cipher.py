from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from ports import CipherPort


class AesCipherAdapter(CipherPort):
    """
    Adaptador para o padrão AES (Advanced Encryption Standard).
    Utiliza AES-256 no modo CTR para uma comparação justa de fluxo/blocos.
    """
    
    def __init__(self):
        # Usamos um nonce/IV fixo estritamente para o teste de benchmark ser determinístico
        self._nonce = b"\x00" * 16

    @property
    def metadata(self) -> dict:
        return {
            "key_size": "256 bits",
            "block_size": "128 bits",
            "parallelization": "Sim (Modo CTR permite paralelização nativa)",
            "diffusion_confusion": "Alta (Provida por Camadas de Substituição [S-Box] e Permutação [MixColumns])",
            "attack_resistance": "Altíssima (Resistente a ataques lineares e diferenciais; imune a ataques quânticos com chaves de 256 bits)",
            "implementation_simplicity": "Baixa/Média (Exige álgebra em Corpos de Galois complexa se feita do zero)",
            "scalability": "Média (Tamanhos de chave fixos em 128, 192, 256 bits)"
        }
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        # Garante que a chave tenha 32 bytes (256 bits) truncando ou completando
        adapted_key = key[:32].ljust(32, b'\x00')
        
        cipher = Cipher(algorithms.AES(adapted_key), modes.CTR(self._nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        return encryptor.update(plaintext) + encryptor.finalize()

    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        adapted_key = key[:32].ljust(32, b'\x00')
        
        cipher = Cipher(algorithms.AES(adapted_key), modes.CTR(self._nonce), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
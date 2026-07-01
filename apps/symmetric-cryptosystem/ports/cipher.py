from abc import ABC, abstractmethod
from typing import Dict


class CipherPort(ABC):
    """
    Porta de saída (Outbound Port) que define a interface comum 
    para todos os algoritmos criptográficos do sistema.
    """

    @property
    @abstractmethod
    def metadata(self) -> Dict[str, str]:
        """
        Retorna um dicionário contendo as propriedades teóricas e estruturais 
        do criptossistema (Tamanho de chave, bloco, paralelização, etc.).
        """
        pass

    @abstractmethod
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Cifra o texto em claro utilizando uma chave secreta."""
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Decifra o texto cifrado utilizando a mesma chave secreta."""
        pass
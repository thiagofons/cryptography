from abc import ABC, abstractmethod


class CipherPort(ABC):
    """
    Porta de saída (Outbound Port) que define a interface comum 
    para todos os algoritmos criptográficos do sistema.
    """

    @abstractmethod
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """
        Cifra o texto em claro utilizando uma chave secreta.

        :param plaintext: Os dados originais em bytes.
        :param key: A chave secreta em bytes.
        :return: O dado cifrado em bytes (ciphertext).
        """
        pass

    @abstractmethod
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """
        Decifra o texto cifrado utilizando a mesma chave secreta.

        :param ciphertext: Os dados criptografados em bytes.
        :param key: A chave secreta em bytes.
        :return: O dado restaurado em bytes (plaintext).
        """
        pass
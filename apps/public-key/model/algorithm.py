from abc import ABC, abstractmethod


class IAlgorithm(ABC):
    def __init__(self):
        self.bit_length: int = 256

    @abstractmethod
    def generate_keys(self) -> tuple:
        """Generate and returns the keys pair (public, private)"""
        pass

    @abstractmethod
    def encrypt(self, plain_text: str, public_key: str) -> str:
        """Cyphers the plain text usig the public key"""
        pass

    @abstractmethod
    def decrypt(self, cipher_text: str, public_key:str, private_key: str) -> str:
        """Decyphers the cipher text using the private key"""
        pass
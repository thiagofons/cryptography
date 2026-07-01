from abc import ABC, abstractmethod


class IAlgorithm(ABC):
    """
    Abstract interface that forces both Diffie-Hellman and ElGamal
    to implement standard key generation and protocol execution.
    """
    @abstractmethod
    def generate_keys(self) -> tuple:
        """Generates and returns a tuple containing (public_key, private_key)."""
        pass

    @abstractmethod
    def run_protocol(self, sender_private_key, recipient_public_key, data=None) -> tuple:
        """Executes the main cryptographic logic (Key Agreement or Encryption/Decryption)."""
        pass
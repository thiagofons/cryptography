import random

from Crypto.Util import number
from model import IAlgorithm


class DiffieHellman(IAlgorithm):
    """
    Pure Diffie-Hellman Key Agreement implementation over the integer multiplicative group.
    """
    def __init__(self, bit_length: int = 256):
        super().__init__()
        self.bit_length = bit_length

    def _find_primitive_root(self, p: int, q: int) -> int:
        """Finds a generator (primitive root) for the group using Fermat's Little Theorem."""
        while True:
            r = random.randint(2, p - 2)
            if pow(r, 2, p) != 1 and pow(r, q, p) != 1:
                return r

    # Modifique apenas o método generate_keys para aceitar parâmetros existentes
    def generate_keys(self, existing_params: tuple = None) -> tuple:
        """
        Requirement 1: Generates or uses safe primes, then creates a keypair.
        If existing_params (p, g) is provided, it stays in the same mathematical group.
        """
        if existing_params:
            # If parameters already exist, reuse them to stay in the identical group
            p, g = existing_params
        else:
            # Otherwise, generate a brand new group from scratch
            while True:
                q = number.getPrime(self.bit_length - 1)
                p = 2 * q + 1
                if number.isPrime(p):
                    break
            g = self._find_primitive_root(p, q)

        private_key = random.randint(3, p - 2)
        public_value = pow(g, private_key, p)

        # Public key packs network parameters (p, g) along with the public value
        public_key = (p, g, public_value)
        return (public_key, private_key)


    def run_protocol(self, sender_private_key: int, recipient_public_key: tuple, data=None) -> int:
        """Requirement 2: Computes the shared secret using the remote public value and local private key."""
        p, g, recipient_public_value = recipient_public_key
        
        # Shared secret = (Y_recipient ^ X_sender) mod p
        shared_secret = pow(recipient_public_value, sender_private_key, p)
        return shared_secret
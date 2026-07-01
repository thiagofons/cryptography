import random

from Crypto.Util import number
from model import IAlgorithm


class ElGamal(IAlgorithm):
    """
    Classic ElGamal Encryption/Decryption implementation over the integer multiplicative group.
    """
    def __init__(self, bit_length: int = 256):
        super().__init__()
        self.bit_length = bit_length

    def _find_primitive_root(self, p: int, q: int) -> int:
        """Finds a generator (primitive root) for the group."""
        while True:
            r = random.randint(2, p - 2)
            if pow(r, 2, p) != 1 and pow(r, q, p) != 1:
                return r

    def generate_keys(self) -> tuple:
        """Generates key pair where public_key is (p, g, y) and private_key is x."""
        while True:
            q = number.getPrime(self.bit_length - 1)
            p = 2 * q + 1
            if number.isPrime(p):
                break

        g = self._find_primitive_root(p, q)
        private_key = random.randint(3, p - 2)
        public_value = pow(g, private_key, p)

        public_key = (p, g, public_value)
        return (public_key, private_key)

    def run_protocol(self, key_component, public_key: tuple, data=None) -> tuple:
        """
        Polymorphic router: Handles encryption if 'data' is a string, 
        or decryption if 'data' is an encrypted tuple (b, c).
        """
        p, g, y = public_key

        if isinstance(data, str):
            text_bytes = data.encode('utf-8')
            message_int = int.from_bytes(text_bytes, byteorder='big')
            
            if message_int >= p:
                raise ValueError("Text string is too long for the selected key bit size!")
                
            k = random.randint(3, p - 2)  # Ephemeral random key
            b = pow(g, k, p)
            c = (message_int * pow(y, k, p)) % p
            return (b, c)

        elif isinstance(data, tuple):
            b, c = data
            private_key = key_component  
            
            # Message = (c * b^(p - 1 - x)) mod p
            exponent = p - 1 - private_key
            decrypted_int = (c * pow(b, exponent, p)) % p
            
            # Decode integer back to plain text string
            byte_length = (decrypted_int.bit_length() + 7) // 8
            decrypted_bytes = decrypted_int.to_bytes(byte_length, byteorder='big')
            return decrypted_bytes.decode('utf-8')
            
        else:
            raise TypeError("Unsupported data type for ElGamal execution.")
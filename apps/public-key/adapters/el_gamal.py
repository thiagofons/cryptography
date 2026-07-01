import random

from Crypto.Util import number
from model import IAlgorithm


class ElGamal(IAlgorithm):
    """
    Implementation of El Gamal algorithm.
    """
    def __init__(self):
        super().__init__()
        # Nota: Presumi que self.bit_length vem da classe pai (IAlgorithm)
        # Se não vier, defina aqui. Ex: self.bit_length = 1024

    def _find_primitive_root(self, p: int, q: int) -> int:
        """ Método privado corrigido com 'self' """
        while True:
            r = random.randint(2, p - 2)
            if pow(r, 2, p) != 1 and pow(r, q, p) != 1:
                return r

    def generate_keys(self) -> tuple:
        # ATENÇÃO: Se bit_length for muito pequeno (ex: < 16), 
        # mude temporariamente a lógica para primos comuns para evitar loops infinitos.
        while True:
            q = number.getPrime(self.bit_length - 1)
            p = 2 * q + 1
            if number.isPrime(p):
                break

        r = self._find_primitive_root(p, q)
        x = random.randint(3, p - 2)
        a = pow(r, x, p)

        return ((p, r, a), x)

    def encrypt(self, plain_text: str, public_key: tuple) -> tuple:
        """ Método corrigido adicionando 'self' """
        p, r, a = public_key
        
        text_bytes = plain_text.encode('utf-8')
        message_int = int.from_bytes(text_bytes, byteorder='big')
        
        if message_int >= p:
            raise ValueError("Text is too long for this key size! Shorten text or increase bit size.")
            
        y = random.randint(3, p - 2)
        b = pow(r, y, p)
        C = (message_int * pow(a, y, p)) % p
        
        return (b, C)
    
    def decrypt(self, cipher_text: tuple, public_key: tuple, private_key: int) -> str:
        """ Método corrigido adicionando 'self' e tipagem correta para o private_key (int) """
        p, _, _ = public_key
        x = private_key  # O private_key deve ser int, não str
        b, C = cipher_text
        
        exponent = p - 1 - x
        decrypted_int = (C * pow(b, exponent, p)) % p
        
        byte_length = (decrypted_int.bit_length() + 7) // 8
        decrypted_bytes = decrypted_int.to_bytes(byte_length, byteorder='big')
        
        return decrypted_bytes.decode('utf-8')

from model import IAlgorithm


class DiffieHellman (IAlgorithm):
    def __init__(self):
        super().__init__() 

    def generate_keys(self):
        raise NotImplementedError

    def encrypt(self, plain_text, public_key):
        raise NotImplementedError

    def decrypt(self, cipher_text, private_key):
        raise NotImplementedError


    
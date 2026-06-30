from model import IAlgorithm


class DiffieHellman (IAlgorithm):
    def __init__(self):
        pass

    def generate_keys(self):
        raise NotImplementedError

    def encrypt(self, plain_text, public_key):
        raise NotImplementedError

    def decrypt(self, cipher_text, private_key):
        raise NotImplementedError


    
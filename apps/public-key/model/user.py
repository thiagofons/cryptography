class User:
    """Represents an entity/participant in the cryptographic communication."""
    
    def __init__(self, name: str):
        self.name = name
        self.public_key = None
        self.__private_key = None  

    def set_keys(self, public_key: tuple, private_key):
        """Stores the key pair assigned to this user."""
        self.public_key = public_key
        self.__private_key = private_key

    def get_private_key(self):
        """Securely exposes the private key when needed by the algorithm."""
        return self.__private_key
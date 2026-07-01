class User:
    def __init__(self, name: str):
        self.name: str = name
        self.public_key: str = None
        self._private_key: str = None

    def set_keys(self, public_key: str, private_key: str):
        """
        Generate both public and private keys for the user
        """
        self.public_key = public_key
        self._private_key = private_key
        pass

    def get_private_key(self):
        return self._private_key

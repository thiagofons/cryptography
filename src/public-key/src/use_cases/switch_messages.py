from model import IAlgorithm, Message, User


class SwitchMessagesUseCase ():
    def __init__(self, algorithm: IAlgorithm, sender: User, receiver: User, message: Message):
        self._algorithm = algorithm
        self._sender = sender
        self._receiver = receiver

    def execute(self, message: Message) -> Message:
        '''
        The sender sends a message to the receiver
        '''
        # 1. Key generation for both users
        public_sender, private_sender = self._algorithm.generate_keys()
        self._sender.set_keys(public_sender, private_sender)

        public_receiver, private_receiver = self._algorithm.generate_keys()
        self._receiver.set_keys(public_receiver, private_receiver)

        print(f"Original text ({self._sender.name}): {message.content}")

        # 2. Cyphering
        encrypted_text = self._algorithm.encrypt(message, public_receiver)
        encrypted_message = Message(content=encrypted_text)

        print(f"In transit (cyphered): {encrypted_message.content}")

        # 3. Decyphering
        decrypted_text = self._algorithm.decrypt(encrypted_message.content, private_receiver)
        decrypted_message = Message(content=decrypted_text)

        print(f"Received and decyphered: {decrypted_message.content}")

        return








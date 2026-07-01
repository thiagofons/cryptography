from model import IAlgorithm, ITerminalPrinter, Message, User


class SwitchMessagesUseCase():
    def __init__(self, algorithm: IAlgorithm, sender: User, receiver: User, printer: ITerminalPrinter):
        self._algorithm = algorithm
        self._sender = sender
        self._receiver = receiver
        self._printer = printer

    def execute(self, message: Message) -> Message:
        '''
        The sender sends a message to the receiver
        '''
        # Título da execução
        self._printer.print_title(f"Fluxo de Troca de Mensagens usando {self._algorithm.__class__.__name__}: {self._sender.name} ➔ {self._receiver.name}")

        # 1. Key generation for both users
        public_sender, private_sender = self._algorithm.generate_keys()
        self._sender.set_keys(public_sender, private_sender)

        public_receiver, private_receiver = self._algorithm.generate_keys()
        self._receiver.set_keys(public_receiver, private_receiver)

        # Primeiro Print (Texto Original)
        self._printer.print_step("Texto Original", message.content)

        # 2. Cyphering
        cipher_tuple = self._algorithm.encrypt(
            plain_text=message.content, 
            public_key=public_receiver
        )
        encrypted_message = Message(content=cipher_tuple)

        # Segundo Print (Em trânsito / Criptografado)
        # Convertemos para string caso cipher_tuple seja uma tupla/objeto complexo
        self._printer.print_alert(f"Em trânsito (Criptografado): {str(encrypted_message.content)}")

        # 3. Decyphering
        decrypted_text = self._algorithm.decrypt(
            cipher_text=encrypted_message.content, 
            public_key=public_receiver,       
            private_key=private_receiver       
        )
        decrypted_message = Message(content=decrypted_text)

        # Terceiro Print (Decifrado com sucesso)
        self._printer.print_step("Texto Recebido/Decifrado", decrypted_message.content)

        return decrypted_message

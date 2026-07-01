from model import IAlgorithm, ITerminalPrinter, Message, User


class ElGamalMessageTransmissionUseCase:
    """
    Orchestrates the classic ElGamal asymmetric message encryption and decryption lifecycle.
    """
    def __init__(self, algorithm: IAlgorithm, sender: User, receiver: User, printer: ITerminalPrinter):
        self._algorithm = algorithm
        self._sender = sender
        self._receiver = receiver
        self._printer = printer

    def execute(self, message: Message):
        self._printer.print_title("ELGAMAL MESSAGE TRANSMISSION")

        # STEP 1: Key generation
        pub_sender, priv_sender = self._algorithm.generate_keys()
        self._sender.set_keys(pub_sender, priv_sender)
        
        pub_receiver, priv_receiver = self._algorithm.generate_keys()
        self._receiver.set_keys(pub_receiver, priv_receiver)
        self._printer.print_step("Environment Setup", f"[{self._receiver.name}] Target keys generated. Ready to receive secure traffic.")

        self._printer.print_alert("Initiating Message Transmission Protocol")
        self._printer.print_step("Input Payload", f"Original Clear Text Message: '{message.content}'")

        # STEP 2: Encryption
        cipher_tuple = self._algorithm.run_protocol(None, pub_receiver, data=message.content)
        encrypted_message = Message(content=cipher_tuple)
        self._printer.print_step("Network Interception", f"Data captured in transit (Encrypted Tuple): {encrypted_message.content}")

        # STEP 3: Decryption
        decrypted_text = self._algorithm.run_protocol(self._receiver.get_private_key(), pub_receiver, data=encrypted_message.content)
        decrypted_message = Message(content=decrypted_text)
        self._printer.print_step(f"Output Payload", f"Decrypted Message recovered by {self._receiver.name}: '{decrypted_message.content}'")

from model import IAlgorithm, ITerminalPrinter, Message, User


class DiffieHellmanKeyExchangeUseCase:
    """
    Orchestrates the pure Diffie-Hellman Key Agreement protocol.
    Demonstrates key generation, public key exchange, and independent secret computation.
    """
    def __init__(self, algorithm: IAlgorithm, sender: User, receiver: User, printer: ITerminalPrinter):
        self._algorithm = algorithm
        self._sender = sender
        self._receiver = receiver
        self._printer = printer

    def execute(self):
        # Displays the main header
        self._printer.print_title("DIFFIE-HELLMAN KEY EXCHANGE")

        # STEP 1: Key generation
        pub_sender, priv_sender = self._algorithm.generate_keys()
        self._sender.set_keys(pub_sender, priv_sender)

        self._printer.print_step(f"{self._sender.name} Key Generation", "Generated Private Key and published parameters (p, g, Y_A).")

        p_group, g_group, _ = pub_sender

        pub_receiver, priv_receiver = self._algorithm.generate_keys(existing_params=(p_group, g_group))
        self._receiver.set_keys(pub_receiver, priv_receiver)
        self._printer.print_step(f"{self._receiver.name} Key Generation", "Generated Private Key and published parameters (p, g, Y_B).")

        # Section Alert
        self._printer.print_alert("Initiating Pure Key Exchange Protocol (Requirement Demonstration)")
        
        # STEP 2: Sender calculates the secret locally using their private key + Receiver public key parameters
        secret_sender = self._algorithm.run_protocol(self._sender.get_private_key(), pub_receiver)
        self._printer.print_step(f"{self._sender.name} Computation", f"Shared Secret computed independently: {secret_sender}")
        
        # STEP 3: Receiver calculates the secret locally using their private key + Sender's public key parameters
        secret_receiver = self._algorithm.run_protocol(self._receiver.get_private_key(), pub_sender)
        self._printer.print_step(f"{self._receiver.name} Computation", f"Shared Secret computed independently: {secret_receiver}")

        # Final Verification and status notification using alerts
        if secret_sender == secret_receiver:
            self._printer.print_alert("SUCCESS: Both parties successfully agreed on the exact same secret integer!")
        else:
            self._printer.print_alert("ERROR: Key exchange mismatched.")


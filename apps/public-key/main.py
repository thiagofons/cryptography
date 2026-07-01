from adapters import DiffieHellman, ElGamal, RichTerminalPrinter
from model import ITerminalPrinter, Message, User
from use_cases import (DiffieHellmanKeyExchangeUseCase,
                       ElGamalMessageTransmissionUseCase)


def main():
    printer: ITerminalPrinter = RichTerminalPrinter()

    alice = User(name="Alice")
    bob = User(name="Bob")

    academic_message = Message(content="Cryptography Homework Sample Text 2026")

    # --- EXECUTION 1: Diffie-Hellman key exchange ---
    dh_algorithm = DiffieHellman(bit_length=256)
    use_case_dh = DiffieHellmanKeyExchangeUseCase(dh_algorithm, sender=alice, receiver=bob, printer=printer)
    use_case_dh.execute()  

    # --- EXECUTION 2: ElGamal message transmission ---
    elgamal_algorithm = ElGamal(bit_length=512)
    use_case_elgamal = ElGamalMessageTransmissionUseCase(elgamal_algorithm, sender=alice, receiver=bob, printer=printer)
    use_case_elgamal.execute(message=academic_message)  
    
    return

if __name__ == "__main__":
    main()
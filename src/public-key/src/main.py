from adapters.algorithms import DiffieHellman, ElGamal
from model import IAlgorithm, Message, User
from use_cases import SwitchMessagesUseCase


def main():
    # Algorithms
    diffie_hellman: IAlgorithm = DiffieHellman()
    el_gamal: IAlgorithm = ElGamal()

    # Users
    alice = User()
    bob = User()

    # Message
    message = Message("Hello, Bob! How are you?")

    # Use cases
    dh_use_case = SwitchMessagesUseCase(
        algorithm=diffie_hellman,
        sender=alice,
        receiver=bob,
    )

    eg_use_case = SwitchMessagesUseCase(
        algorithm=el_gamal,
        sender=alice,
        receiver=bob
    )

    # =======================================
    # 1st round: Diffie Hellman
    # =======================================
    print("Diffie Hellman:")
    dh_use_case.execute(message)

    # =======================================
    # 2nd round: Diffie Hellman
    # =======================================
    print("El Gamal:")
    eg_use_case.execute(message)

    return

if __name__ == "__main__":
    main()
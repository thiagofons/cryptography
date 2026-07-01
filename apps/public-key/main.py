from adapters import DiffieHellman, ElGamal
from model import IAlgorithm, Message, User
from use_cases import SwitchMessagesUseCase


def main():
    # Algorithms
    el_gamal: IAlgorithm = ElGamal()
    diffie_hellman: IAlgorithm = DiffieHellman()

    # Users
    alice = User(name="Alice")
    bob = User(name="Bob")

    # Message
    message = Message("Hello, Bob! How are you?")

    # Use cases
    eg_use_case = SwitchMessagesUseCase(
        algorithm=el_gamal,
        sender=alice,
        receiver=bob
    )
    # dh_use_case = SwitchMessagesUseCase(
    #     algorithm=diffie_hellman,
    #     sender=alice,
    #     receiver=bob,
    # )

    # =======================================
    # 1st round: El Gamal
    # =======================================
    print("El Gamal:")
    eg_use_case.execute(message)

    # =======================================
    # 2nd round: Diffie Hellman
    # =======================================
    # print("Diffie Hellman:")
    # dh_use_case.execute(message)
    
    return

if __name__ == "__main__":
    main()
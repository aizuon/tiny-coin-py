import base58

__table = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz".encode("ascii")


def base58_encode(buffer: bytes) -> str:
    return base58.b58encode(buffer, alphabet=__table).decode("ascii")

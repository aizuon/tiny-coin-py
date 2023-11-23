import base58

from tiny_coin.utils import bytes_to_str, str_to_bytes

__table = str_to_bytes("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")


def base58_encode(buffer: bytes) -> str:
    return bytes_to_str(base58.b58encode(buffer, alphabet=__table))

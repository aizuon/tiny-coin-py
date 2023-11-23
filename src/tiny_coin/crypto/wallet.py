from tiny_coin.crypto.base58_ext import base58_encode
from tiny_coin.crypto.ripemd160_ext import ripemd160_hash_binary
from tiny_coin.crypto.sha256_ext import sha256_double_hash_binary, sha256_hash_binary

__pub_key_hash_version = "1"


def pub_key_to_address(pub_key: bytes):
    sha256 = sha256_hash_binary(pub_key)

    ripemd160 = ripemd160_hash_binary(sha256)

    checksum = sha256_double_hash_binary(b"\x00" + ripemd160)[:4]

    ripemd160 = ripemd160 + checksum

    return __pub_key_hash_version + base58_encode(ripemd160)

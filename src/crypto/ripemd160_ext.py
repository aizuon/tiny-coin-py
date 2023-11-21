import hashlib


def ripemd160_hash_binary(buffer: bytes):
    return hashlib.new("ripemd160", buffer).digest()

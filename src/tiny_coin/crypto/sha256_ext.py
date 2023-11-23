from hashlib import sha256


def sha256_hash_binary(buffer: bytes):
    return sha256(buffer).digest()


def sha256_double_hash_binary(buffer: bytes):
    return sha256_hash_binary(sha256_hash_binary(buffer))

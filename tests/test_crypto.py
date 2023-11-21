from src.crypto.base58_ext import base58_encode
from src.crypto.ecdsa_ext import (
    ecdsa_generate,
    ecdsa_get_pub_key_from_priv_key,
    ecdsa_sign_msg,
    ecdsa_verify_sig,
)
from src.crypto.ripemd160_ext import ripemd160_hash_binary
from src.crypto.sha256_ext import sha256_double_hash_binary, sha256_hash_binary


def test_sha256_hashing():
    hash = sha256_hash_binary("foo".encode("ascii")).hex()

    assert hash == "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"


def test_sha256d_hashing():
    hash = sha256_double_hash_binary("foo".encode("ascii")).hex()

    assert hash == "c7ade88fc7a21498a6a5e5c385e1f68bed822b72aa63c4a9a48a02c2466ee29e"


def test_ripemd160_hashing():
    hash = ripemd160_hash_binary("foo".encode("ascii")).hex()

    assert hash == "42cfa211018ea492fdee45ac637b7972a0ad6873"


def test_base58_encode():
    hash = base58_encode("foo".encode("ascii"))

    assert hash == "bQbp"


def test_ecdsa_key_pair_generation():
    priv_key, pub_key = ecdsa_generate()

    priv_key_str = priv_key.hex()
    pub_key_str = pub_key.hex()

    assert priv_key_str
    assert pub_key_str


def test_ecdsa_get_pub_key_from_priv_key():
    priv_key, pub_key = ecdsa_generate()

    pub_key_str = pub_key.hex()

    pub_key_from_priv_key = ecdsa_get_pub_key_from_priv_key(priv_key).hex()

    assert pub_key_str
    assert pub_key_from_priv_key
    assert pub_key_from_priv_key == pub_key_str


def test_ecdsa_signing_and_verification():
    priv_key, pub_key = ecdsa_generate()

    msg = "foo".encode("ascii")

    sig = ecdsa_sign_msg(msg, priv_key)

    assert sig
    assert ecdsa_verify_sig(sig, msg, pub_key)

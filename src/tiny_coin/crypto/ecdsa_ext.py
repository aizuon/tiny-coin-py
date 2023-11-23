from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)


def ecdsa_generate():
    priv_key = ec.generate_private_key(ec.SECP256K1())
    pub_key = priv_key.public_key()

    priv_key_buffer = priv_key.private_bytes(
        Encoding.DER, PrivateFormat.PKCS8, NoEncryption()
    )
    pub_key_buffer = pub_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    return priv_key_buffer, pub_key_buffer


def ecdsa_get_pub_key_from_priv_key(priv_key_buffer: bytes):
    priv_key = serialization.load_der_private_key(priv_key_buffer, password=None)
    pub_key = priv_key.public_key()

    pub_key_buffer = pub_key.public_bytes(Encoding.X962, PublicFormat.CompressedPoint)

    return pub_key_buffer


def ecdsa_sign_msg(msg: bytes, priv_key_buffer: bytes) -> bytes:
    priv_key = serialization.load_der_private_key(priv_key_buffer, password=None)
    sig = priv_key.sign(msg, ec.ECDSA(hashes.SHA256()))

    return sig


def ecdsa_verify_sig(sig: bytes, msg: bytes, pub_key_buffer: bytes):
    pub_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256K1(), pub_key_buffer
    )
    try:
        pub_key.verify(sig, msg, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False

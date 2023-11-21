from src.crypto.wallet import pub_key_to_address


def test_pub_key_to_address():
    pub_key = bytes.fromhex(
        "0250863ad64a87ae8a2fe83c1af1a8403cb53f53e486d8511dad8a04887e5b2352"
    )

    address = pub_key_to_address(pub_key)

    assert address == "1PMycacnJaSqwwJqjawXBErnLsZ7RkXUAs"

from tiny_coin.crypto.merkle_tree import MerkleTree
from tiny_coin.crypto.sha256_ext import sha256_double_hash_binary
from tiny_coin.utils import str_to_bytes


def test_one_chain():
    foo = "foo"
    bar = "bar"
    tree = [foo, bar]

    root = MerkleTree.get_root(tree)
    foo_h = sha256_double_hash_binary(str_to_bytes(foo)).hex()
    bar_h = sha256_double_hash_binary(str_to_bytes(bar)).hex()

    combined_h = sha256_double_hash_binary(str_to_bytes(foo_h + bar_h)).hex()
    assert combined_h == root.value
    assert foo_h == root.children[0].value
    assert bar_h == root.children[1].value


def test_two_chain():
    foo = "foo"
    bar = "bar"
    baz = "baz"
    tree = [foo, bar, baz]

    root = MerkleTree.get_root(tree)
    foo_h = sha256_double_hash_binary(str_to_bytes(foo)).hex()
    bar_h = sha256_double_hash_binary(str_to_bytes(bar)).hex()
    baz_h = sha256_double_hash_binary(str_to_bytes(baz)).hex()

    assert len(root.children) == 2
    combined_h1 = sha256_double_hash_binary(str_to_bytes(foo_h + bar_h)).hex()
    combined_h2 = sha256_double_hash_binary(str_to_bytes(baz_h + baz_h)).hex()
    assert combined_h1 == root.children[0].value
    assert combined_h2 == root.children[1].value

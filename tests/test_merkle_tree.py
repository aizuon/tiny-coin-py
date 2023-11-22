from src.crypto.merkle_tree import MerkleTree
from src.crypto.sha256_ext import sha256_double_hash_binary


def test_one_chain():
    foo = "foo"
    bar = "bar"
    tree = [foo, bar]

    root = MerkleTree.get_root(tree)
    foo_h = sha256_double_hash_binary(foo.encode("ascii")).hex()
    bar_h = sha256_double_hash_binary(bar.encode("ascii")).hex()

    combined_h = sha256_double_hash_binary((foo_h + bar_h).encode("ascii")).hex()
    assert combined_h == root.value
    assert foo_h == root.children[0].value
    assert bar_h == root.children[1].value


def test_two_chain():
    foo = "foo"
    bar = "bar"
    baz = "baz"
    tree = [foo, bar, baz]

    root = MerkleTree.get_root(tree)
    foo_h = sha256_double_hash_binary(foo.encode("ascii")).hex()
    bar_h = sha256_double_hash_binary(bar.encode("ascii")).hex()
    baz_h = sha256_double_hash_binary(baz.encode("ascii")).hex()

    assert len(root.children) == 2
    combined_h1 = sha256_double_hash_binary((foo_h + bar_h).encode("ascii")).hex()
    combined_h2 = sha256_double_hash_binary((baz_h + baz_h).encode("ascii")).hex()
    assert combined_h1 == root.children[0].value
    assert combined_h2 == root.children[1].value

from tiny_coin.crypto.sha256_ext import sha256_double_hash_binary
from tiny_coin.utils import str_to_bytes


class MerkleNode:
    def __init__(self, value: str, children: list["MerkleNode"] = None):
        self.value = value
        if children is None:
            children = []
        self.children = children


class MerkleTree:
    @staticmethod
    def get_root(leaves: list[str]):
        nodes = []
        for leaf in leaves:
            node = MerkleNode(sha256_double_hash_binary(str_to_bytes(leaf)).hex())
            nodes.append(node)
        return __class__._find_root(nodes)

    @staticmethod
    def _chunk(nodes: list[MerkleNode], chunk_size: int) -> list[list[MerkleNode]]:
        chunks = []

        chunk = []
        for node in nodes:
            chunk.append(node)
            if len(chunk) == chunk_size:
                chunks.append(chunk)
                chunk = []

        if chunk:
            while len(chunk) != chunk_size:
                chunk.append(chunk[-1])
            chunks.append(chunk)

        return chunks

    @staticmethod
    def _find_root(nodes: list[MerkleNode]) -> MerkleNode:
        chunks = __class__._chunk(nodes, 2)
        new_level = []
        for chunk in chunks:
            combined_id = ""
            for node in chunk:
                combined_id += node.value

            combined_hash = sha256_double_hash_binary(str_to_bytes(combined_id)).hex()

            node = MerkleNode(combined_hash, chunk)

            new_level.append(node)

        return __class__._find_root(new_level) if len(new_level) > 1 else new_level[0]

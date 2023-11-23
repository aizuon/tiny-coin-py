from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import int64
from tiny_coin.serializable import Serializable


class TxOutPoint(Serializable, Deserializable):
    def __init__(self, tx_id: str = None, tx_out_idx: int = -1) -> None:
        super().__init__()
        if tx_id is None:
            tx_id = ""
        self.tx_id = tx_id
        self.tx_out_idx = int64(tx_out_idx)

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return self.tx_id == other.tx_id and self.tx_out_idx == other.tx_out_idx

    def serialize(self):
        buffer = BinaryBuffer()

        buffer.write(self.tx_id)
        buffer.write(self.tx_out_idx)

        return buffer

    @staticmethod
    def deserialize(buffer: BinaryBuffer):
        tx_out_point = __class__()

        tx_out_point.tx_id = buffer.read()
        if tx_out_point.tx_id is None:
            return None
        tx_out_point.tx_out_idx = buffer.read(int64)
        if tx_out_point.tx_out_idx is None:
            return None

        return tx_out_point

from dataclasses import dataclass, field

from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import int64
from tiny_coin.serializable import Serializable


@dataclass(eq=False)
class TxOutPoint(Serializable, Deserializable):
    tx_id: str = field(default_factory=str)
    tx_out_idx: int | int64 = -1

    def __post_init__(self):
        self.tx_out_idx = int64(self.tx_out_idx)

    def serialize(self):
        buffer = BinaryBuffer()

        buffer.write(self.tx_id)
        buffer.write(self.tx_out_idx)

        return buffer

    @staticmethod
    def deserialize(buffer: BinaryBuffer):
        tx_out_point = __class__()

        tx_out_point.tx_id = buffer.read(str)
        if tx_out_point.tx_id is None:
            return None
        tx_out_point.tx_out_idx = buffer.read(int64)
        if tx_out_point.tx_out_idx is None:
            return None

        return tx_out_point

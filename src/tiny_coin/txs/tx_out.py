from dataclasses import dataclass, field

from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import uint64
from tiny_coin.serializable import Serializable


@dataclass(eq=False)
class TxOut(Serializable, Deserializable):
    value: int | uint64 = 0
    to_address: str = field(default_factory=str)

    def __post_init__(self):
        self.value = uint64(self.value)

    def serialize(self):
        buffer = BinaryBuffer()

        buffer.write(self.value)
        buffer.write(self.to_address)

        return buffer

    @staticmethod
    def deserialize(buffer: BinaryBuffer):
        tx_out = __class__()

        tx_out.value = buffer.read(uint64)
        if tx_out.value is None:
            return None
        tx_out.to_address = buffer.read(str)
        if tx_out.to_address is None:
            return None

        return tx_out

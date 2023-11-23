from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import uint64
from tiny_coin.serializable import Serializable


class TxOut(Serializable, Deserializable):
    def __init__(self, value: int = 0, to_address: str = None) -> None:
        super().__init__()
        if to_address is None:
            to_address = ""
        self.value = uint64(value)
        self.to_address = to_address

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return self.value == other.value and self.to_address == other.to_address

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

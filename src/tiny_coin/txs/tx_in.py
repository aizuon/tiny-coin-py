from dataclasses import dataclass, field

from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import bool8, int32
from tiny_coin.serializable import Serializable
from tiny_coin.txs.tx_out_point import TxOutPoint


@dataclass(eq=False)
class TxIn(Serializable, Deserializable):
    to_spend: TxOutPoint = None
    unlock_sig: bytearray = field(default_factory=bytearray)
    unlock_pub_key: bytearray = field(default_factory=bytearray)
    sequence: int | int32 = -1

    def __post_init__(self):
        self.sequence = int32(self.sequence)

    def serialize(self):
        buffer = BinaryBuffer()

        has_to_spend = bool8(self.to_spend is not None)
        buffer.write(has_to_spend)
        if has_to_spend.value is True:
            buffer.write_raw(self.to_spend.serialize().buffer)
        buffer.write(self.unlock_sig)
        buffer.write(self.unlock_pub_key)
        buffer.write(self.sequence)

        return buffer

    @staticmethod
    def deserialize(buffer: BinaryBuffer):
        tx_in = __class__()

        has_to_spend = buffer.read(bool8)
        if has_to_spend is None:
            return None
        if has_to_spend.value is True:
            tx_in.to_spend = TxOutPoint.deserialize(buffer)
            if tx_in.to_spend is None:
                return None
        tx_in.unlock_sig = buffer.read(bytearray)
        if tx_in.unlock_sig is None:
            return None
        tx_in.unlock_pub_key = buffer.read(bytearray)
        if tx_in.unlock_pub_key is None:
            return None
        tx_in.sequence = buffer.read(int32)
        if tx_in.sequence is None:
            return None

        return tx_in

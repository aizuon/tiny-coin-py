from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import int32
from tiny_coin.serializable import Serializable
from tiny_coin.tx.tx_out_point import TxOutPoint


class TxIn(Serializable, Deserializable):
    def __init__(
        self,
        to_spend: TxOutPoint = None,
        unlock_sig: bytearray = None,
        unlock_pub_key: bytearray = None,
        sequence: int = -1,
    ) -> None:
        super().__init__()
        self.to_spend = to_spend
        if unlock_sig is None:
            unlock_sig = bytearray()
        self.unlock_sig = unlock_sig
        if unlock_pub_key is None:
            unlock_pub_key = bytearray()
        self.unlock_pub_key = unlock_pub_key
        self.sequence = int32(sequence)

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return (
            self.to_spend == other.to_spend
            and self.unlock_sig == other.unlock_sig
            and self.unlock_pub_key == other.unlock_pub_key
        )

    def serialize(self):
        buffer = BinaryBuffer()

        has_to_spend = self.to_spend is not None
        buffer.write(has_to_spend)
        if has_to_spend:
            buffer.write_raw(self.to_spend.serialize().buffer)
        buffer.write(self.unlock_sig)
        buffer.write(self.unlock_pub_key)
        buffer.write(self.sequence)

        return buffer

    @staticmethod
    def deserialize(buffer: BinaryBuffer):
        tx_in = __class__()

        has_to_spend = buffer.read(bool)
        if has_to_spend is None:
            return None
        if has_to_spend is True:
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

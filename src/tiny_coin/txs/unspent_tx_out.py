from dataclasses import dataclass

from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import bool8, int64
from tiny_coin.serializable import Serializable
from tiny_coin.txs.tx_out import TxOut
from tiny_coin.txs.tx_out_point import TxOutPoint


@dataclass(eq=False)
class UnspentTxOut(Serializable, Deserializable):
    tx_out: TxOut = None
    tx_out_point: TxOutPoint = None
    is_coinbase: bool | bool8 = False
    height: int | int64 = -1

    def __post_init__(self):
        self.is_coinbase = bool8(self.is_coinbase)
        self.height = int64(self.height)

    def serialize(self):
        buffer = BinaryBuffer()

        buffer.write_raw(self.tx_out.serialize().buffer)
        buffer.write_raw(self.tx_out_point.serialize().buffer)
        buffer.write(self.is_coinbase)
        buffer.write(self.height)

        return buffer

    @staticmethod
    def deserialize(buffer: BinaryBuffer):
        utxo = __class__()

        utxo.tx_out = TxOut.deserialize(buffer)
        if utxo.tx_out is None:
            return None
        utxo.tx_out_point = TxOutPoint.deserialize(buffer)
        if utxo.tx_out_point is None:
            return None
        utxo.is_coinbase = buffer.read(bool8)
        if utxo.is_coinbase is None:
            return None
        utxo.height = buffer.read(int64)
        if utxo.height is None:
            return None

        return utxo


UTXO = UnspentTxOut

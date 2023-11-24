from dataclasses import dataclass, field

from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.crypto.sha256_ext import sha256_double_hash_binary
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import int64
from tiny_coin.serializable import Serializable
from tiny_coin.txs.tx_in import TxIn
from tiny_coin.txs.tx_out import TxOut


@dataclass(eq=False)
class Tx(Serializable, Deserializable):
    tx_ins: list[TxIn] = field(default_factory=list)
    tx_outs: list[TxOut] = field(default_factory=list)
    lock_time: int | int64 = 0

    def __post_init__(self):
        self.lock_time = int64(self.lock_time)

    @property
    def is_coinbase(self):
        return len(self.tx_ins) == 1 and self.tx_ins[0].to_spend is None

    @property
    def id(self):
        return sha256_double_hash_binary(self.serialize().buffer).hex()

    def serialize(self):
        buffer = BinaryBuffer()

        buffer.write_size(len(self.tx_ins))
        for tx_in in self.tx_ins:
            buffer.write_raw(tx_in.serialize().buffer)

        buffer.write_size(len(self.tx_outs))
        for tx_out in self.tx_outs:
            buffer.write_raw(tx_out.serialize().buffer)

        buffer.write(self.lock_time)

        return buffer

    @staticmethod
    def deserialize(buffer: BinaryBuffer):
        tx = __class__()

        tx_ins_size = buffer.read_size()
        tx.tx_ins = []
        for _ in range(tx_ins_size):
            tx_in = TxIn.deserialize(buffer)
            if tx_in is None:
                return None
            tx.tx_ins.append(tx_in)

        tx_outs_size = buffer.read_size()
        tx.tx_outs = []
        for _ in range(tx_outs_size):
            tx_out = TxOut.deserialize(buffer)
            if tx_out is None:
                return None
            tx.tx_outs.append(tx_out)

        tx.lock_time = buffer.read(int64)
        if tx.lock_time is None:
            return None

        return tx

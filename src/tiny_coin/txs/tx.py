from dataclasses import dataclass, field

from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.crypto.ecdsa_ext import ecdsa_verify_sig
from tiny_coin.crypto.sha256_ext import sha256_double_hash_binary
from tiny_coin.crypto.wallet import pub_key_to_address
from tiny_coin.deserializable import Deserializable
from tiny_coin.generics import int64, uint64
from tiny_coin.net_params import NetParams
from tiny_coin.p2p.msg_serializer import MsgSerializer
from tiny_coin.serializable import Serializable
from tiny_coin.txs.tx_in import TxIn
from tiny_coin.txs.tx_out import TxOut
from tiny_coin.txs.unspent_tx_out import UTXO


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

    @staticmethod
    def create_coinbase(pay_to_addr: str, value: uint64, height: int64):
        tx_in_unlock_sig = BinaryBuffer()
        tx_in_unlock_sig.write(height)
        tx_in = TxIn(None, tx_in_unlock_sig.buffer, bytearray(), -1)

        tx_out = TxOut(value, pay_to_addr)

        tx_ins = [tx_in]
        tx_outs = [tx_out]
        tx = __class__(tx_ins, tx_outs, 0)

        return tx

    def validate_basics(self, is_coinbase: bool = False):
        if not self.tx_outs or (not self.tx_ins and not is_coinbase):
            raise TxValidationException("Missing TxOuts or TxIns")

        if self.serialize().size > NetParams.MAX_BLOCK_SERIALIZED_SIZE_IN_BYTES:
            raise TxValidationException("Too large")

        total_spend = uint64(0)
        for tx_out in self.tx_outs:
            total_spend.value += tx_out.value.value

        if total_spend.value > NetParams.MAX_MONEY:
            raise TxValidationException("Spend value too high")

    def __validate_sig_for_spend(self, tx_in: TxIn, utxo: UTXO):
        pub_key_as_addr = pub_key_to_address(tx_in.unlock_pub_key)
        if pub_key_as_addr != utxo.tx_out.to_address:
            raise TxUnlockException("Public key does not match")

        spend_msg = MsgSerializer.build_spend_msg(
            tx_in.to_spend, tx_in.unlock_pub_key, tx_in.sequence, self.tx_outs
        )
        if not ecdsa_verify_sig(tx_in.unlock_sig, spend_msg, tx_in.unlock_pub_key):
            raise TxUnlockException("Signature does not match")


class TxUnlockException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class TxValidationException(Exception):
    def __init__(self, msg: str, to_orphan: Tx = None):
        super().__init__(msg)
        self.to_orphan = to_orphan

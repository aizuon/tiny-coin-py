from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.crypto.sha256_ext import sha256_double_hash_binary
from tiny_coin.generics import int32
from tiny_coin.txs.tx_out import TxOut
from tiny_coin.txs.tx_out_point import TxOutPoint


class MsgSerializer:
    @staticmethod
    def build_spend_msg(
        to_spend: TxOutPoint,
        pub_key: bytearray | bytes,
        sequence: int32,
        tx_outs: list[TxOut],
    ):
        spend_msg = BinaryBuffer()
        spend_msg.write_raw(to_spend.serialize().buffer)
        spend_msg.write(sequence)
        spend_msg.write(pub_key)
        for tx_out in tx_outs:
            spend_msg.write_raw(tx_out.serialize().buffer)

        buffer = spend_msg.buffer

        sha256d = sha256_double_hash_binary(buffer)

        return sha256d

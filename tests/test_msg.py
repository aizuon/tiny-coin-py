from tiny_coin.p2p.msg_serializer import MsgSerializer
from tiny_coin.txs.tx import Tx
from tiny_coin.txs.tx_in import TxIn
from tiny_coin.txs.tx_out import TxOut
from tiny_coin.txs.tx_out_point import TxOutPoint


def test_spend_msg():
    to_spend = TxOutPoint("foo", 0)

    tx_ins = []
    tx_in = TxIn(to_spend, bytearray(), bytearray(), -1)
    tx_ins.append(tx_in)

    tx_outs = []
    tx_out = TxOut(0, "foo")
    tx_outs.append(tx_out)

    tx = Tx(tx_ins, tx_outs, 0)

    spend_msg = MsgSerializer.build_spend_msg(
        tx_in.to_spend, tx_in.unlock_pub_key, tx_in.sequence, tx.tx_outs
    )
    spend_msg_str = spend_msg.hex()

    assert (
        spend_msg_str
        == "d2cde10c62cdc1707ad78d7356e01a73d1376a7a1f775ca6d207d8a511fdff19"
    )

    tx_out2 = TxOut(0, "foo")
    tx.tx_outs.append(tx_out2)

    spend_msg2 = MsgSerializer.build_spend_msg(
        tx_in.to_spend, tx_in.unlock_pub_key, tx_in.sequence, tx.tx_outs
    )
    spend_msg2_str = spend_msg2.hex()

    assert spend_msg_str != spend_msg2_str

from tiny_coin.txs.tx import Tx
from tiny_coin.txs.tx_in import TxIn
from tiny_coin.txs.tx_out import TxOut
from tiny_coin.txs.tx_out_point import TxOutPoint
from tiny_coin.txs.unspent_tx_out import UTXO


def test_tx_serialization():
    tx_ins = [TxIn(TxOutPoint("foo", 0), bytearray(), bytearray(), -1)]
    tx_outs = [TxOut(0, "foo")]
    tx = Tx(tx_ins, tx_outs, 0)

    serialized_buffer = tx.serialize()

    tx2 = Tx.deserialize(serialized_buffer)
    assert tx == tx2


def test_tx_in_serialization():
    to_spend = TxOutPoint("foo", 0)
    tx_in = TxIn(to_spend, bytearray(), bytearray(), -1)

    serialized_buffer = tx_in.serialize()

    tx_in2 = TxIn.deserialize(serialized_buffer)
    assert tx_in == tx_in2


def test_tx_out_serialization():
    tx_out = TxOut(0, "foo")

    serialized_buffer = tx_out.serialize()

    tx_out2 = TxOut.deserialize(serialized_buffer)
    assert tx_out == tx_out2


def test_tx_out_point_serialization():
    tx_out_point = TxOutPoint("foo", 0)

    serialized_buffer = tx_out_point.serialize()

    tx_out_point2 = TxOutPoint.deserialize(serialized_buffer)
    assert tx_out_point == tx_out_point2


def test_utxo_serialization():
    tx_out = TxOut(0, "foo")
    tx_out_point = TxOutPoint("foo", 0)
    utxo = UTXO(tx_out, tx_out_point, False, -1)

    serialized_buffer = utxo.serialize()

    utxo2 = UTXO.deserialize(serialized_buffer)
    assert utxo == utxo2

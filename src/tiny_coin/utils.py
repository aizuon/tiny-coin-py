from tiny_coin.generics import (
    bool8,
    double64,
    float32,
    int8,
    int16,
    int32,
    int64,
    uint8,
    uint16,
    uint32,
    uint64,
)


def str_to_bytes(s: str):
    return s.encode("ascii")


def bytes_to_str(b: bytes):
    return b.decode("ascii")


def list_to_type[
    T: (
        bool8,
        int8,
        int16,
        int32,
        int64,
        uint8,
        uint16,
        uint32,
        uint64,
        float32,
        double64,
    )
](l: list[int | float], t: T,) -> list[T] | bytearray:
    if t == uint8:
        l_c = bytearray(o for o in l)
    else:
        l_c = [t(o) for o in l]
    return l_c

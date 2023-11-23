from abc import ABC


class Generic[T](ABC):
    value: T
    fmt: str

    def __init__(self, value: T = None):
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return self.value == other.value

    def __repr__(self) -> str:
        return super().__repr__() + f"({self.value})"

    def __str__(self) -> str:
        return super().__str__() + f"({self.value})"


class bool8(Generic[bool]):
    fmt = "<?"


class int8(Generic[int]):
    fmt = "<b"


class int16(Generic[int]):
    fmt = "<h"


class int32(Generic[int]):
    fmt = "<i"


class int64(Generic[int]):
    fmt = "<q"


class uint8(Generic[int]):
    fmt = "<B"


class uint16(Generic[int]):
    fmt = "<H"


class uint32(Generic[int]):
    fmt = "<I"


class uint64(Generic[int]):
    fmt = "<Q"


class float32(Generic[float]):
    fmt = "<f"


class double64(Generic[float]):
    fmt = "<d"

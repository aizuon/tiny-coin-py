from abc import ABC, abstractmethod

from tiny_coin.binary_buffer import BinaryBuffer


class Serializable(ABC):
    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return self.serialize() == other.serialize()

    @abstractmethod
    def serialize(self) -> BinaryBuffer:
        ...

from abc import ABC, abstractmethod

from tiny_coin.binary_buffer import BinaryBuffer


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> BinaryBuffer:
        ...

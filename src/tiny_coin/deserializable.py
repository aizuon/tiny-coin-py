from abc import ABC, abstractmethod

from tiny_coin.binary_buffer import BinaryBuffer


class Deserializable(ABC):
    @staticmethod
    @abstractmethod
    def deserialize(buffer: BinaryBuffer):
        ...

import struct
from threading import RLock
from typing import Iterable, get_args, get_origin

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
from tiny_coin.utils import bytes_to_str, str_to_bytes


class BinaryBuffer:
    def __init__(self, buffer: bytearray | bytes = None):
        self._buffer = bytearray(buffer) if buffer else bytearray()
        self._write_offset = len(self._buffer)
        self._read_offset = 0
        self._lock = RLock()

    def __eq__(self, other):
        if not isinstance(other, BinaryBuffer):
            return False
        return (
            self._buffer == other._buffer
            and self._write_offset == other._write_offset
            and self._read_offset == other._read_offset
        )

    @property
    def buffer(self):
        return self._buffer

    @property
    def size(self):
        return len(self._buffer)

    @property
    def write_offset(self):
        return self._write_offset

    @property
    def read_offset(self):
        return self._read_offset

    def grow_to(self, size: int):
        with self._lock:
            assert size > len(self._buffer)
            self._buffer.extend(bytearray(size - len(self._buffer)))

    def reserve(self, size: int):
        with self._lock:
            self._buffer.extend(bytearray(size))

    def write_size(self, obj: int):
        with self._lock:
            self.write(uint32(obj))

    def write(
        self,
        obj: bool8
        | int8
        | int16
        | int32
        | int64
        | uint8
        | uint16
        | uint32
        | uint64
        | float32
        | double64
        | list
        | bytearray
        | bytes
        | str,
    ):
        with self._lock:
            if isinstance(obj, str):
                self._write_string(obj)
            elif (
                isinstance(obj, list)
                or isinstance(obj, bytearray)
                or isinstance(obj, bytes)
            ):
                self._write_array(obj)
            else:
                data = struct.pack(obj.fmt, obj.value)
                self._grow_if_needed(len(data))
                self._buffer[self._write_offset : self._write_offset + len(data)] = data
                self._write_offset += len(data)

    def _write_array(self, obj: Iterable):
        with self._lock:
            if isinstance(obj, bytearray) | isinstance(obj, bytes):
                obj = [uint8(o) for o in obj]
            size = len(obj)
            self.write_size(size)
            for o in obj:
                self.write(o)

    def _write_array_raw(self, obj: Iterable):
        with self._lock:
            if isinstance(obj, bytearray) | isinstance(obj, bytes):
                obj = [uint8(o) for o in obj]
            for o in obj:
                self.write(o)

    def write_raw(self, obj: Iterable | str):
        with self._lock:
            if isinstance(obj, str):
                return self._write_string_raw(obj)
            elif (
                isinstance(obj, list)
                or isinstance(obj, bytearray)
                or isinstance(obj, bytes)
            ):
                return self._write_array_raw(obj)
            else:
                raise ValueError(f"Unsupported object type: {type(obj)}")

    def _write_string(self, obj: str):
        with self._lock:
            self._write_array(str_to_bytes(obj))

    def _write_string_raw(self, obj: str):
        with self._lock:
            self._write_array_raw(str_to_bytes(obj))

    def read_size(self):
        with self._lock:
            size = self.read(uint32)
            if size is None:
                return None
            return size.value

    def read(
        self,
        obj_type: bool8
        | int8
        | int16
        | int32
        | int64
        | uint8
        | uint16
        | uint32
        | uint64
        | float32
        | double64
        | list
        | bytearray
        | bytes
        | str,
    ) -> (
        bool8
        | int8
        | int16
        | int32
        | int64
        | uint8
        | uint16
        | uint32
        | uint64
        | float32
        | double64
        | list
        | bytearray
        | bytes
        | str
    ):
        with self._lock:
            if obj_type == str:
                return self._read_string()
            elif get_origin(obj_type) is list:
                args = get_args(obj_type)
                if len(args) != 1:
                    raise ValueError(f"Unsupported list type: {obj_type}")
                underlying_type = args[0]
                return self._read_array(underlying_type)
            elif obj_type == bytearray or obj_type == bytes:
                return self._read_array(uint8)
            fmt = obj_type.fmt
            size = struct.calcsize(fmt)
            if len(self._buffer) < self._read_offset + size:
                return None
            data = self._buffer[self._read_offset : self._read_offset + size]
            self._read_offset += size
            return obj_type(struct.unpack(fmt, data)[0])

    def _read_array[T](self, obj_type: type[T]) -> Iterable[T]:
        with self._lock:
            size = self.read_size()
            if size is None:
                return None
            if obj_type == uint8:
                result = bytearray()
            else:
                result = []
            for _ in range(size):
                item = self.read(obj_type)
                if item is None:
                    return None
                if obj_type == uint8:
                    result.append(item.value)
                else:
                    result.append(item)
            return result

    def _read_string(self):
        with self._lock:
            result = self._read_array(uint8)
            return bytes_to_str(result) if result is not None else None

    def _grow_if_needed(self, write_length: int):
        with self._lock:
            final_length = self._write_offset + write_length
            resize_needed = len(self._buffer) <= final_length

            if resize_needed:
                self._buffer.extend(bytearray(final_length - len(self._buffer)))

import struct
from threading import RLock


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
        assert size > len(self._buffer)
        self._buffer.extend(bytearray(size - len(self._buffer)))

    def reserve(self, size: int):
        self._buffer.extend(bytearray(size))

    def write_size(self, obj: int):
        self.write(obj, num_bytes=4, signed=False)

    def write(self, obj, num_bytes: int = None, signed: bool = True):
        with self._lock:
            fmt = self._get_format_from_bytes(type(obj), num_bytes, signed)
            data = struct.pack(fmt, obj)
            self._grow_if_needed(len(data))
            self._buffer[self._write_offset : self._write_offset + len(data)] = data
            self._write_offset += len(data)

    def write_list(self, obj: list, num_bytes: int = None, signed: bool = True):
        with self._lock:
            size = len(obj)
            self.write_size(size)
            for o in obj:
                self.write(o, num_bytes=num_bytes, signed=signed)

    def write_raw(self, obj: list, num_bytes: int = None, signed: bool = True):
        with self._lock:
            for o in obj:
                self.write(o, num_bytes=num_bytes, signed=signed)

    def write_string(self, obj: str):
        self.write_list(obj.encode("ascii"), 1, False)

    def write_raw_string(self, obj: str):
        self.write_raw(obj.encode("ascii"), 1, False)

    def read_size(self):
        return self.read(int, num_bytes=4, signed=False)

    def read[
        T
    ](self, obj_type: type[T], num_bytes: int = None, signed: bool = True) -> T:
        with self._lock:
            fmt = self._get_format_from_bytes(obj_type, num_bytes, signed)
            size = struct.calcsize(fmt)
            if len(self._buffer) < self._read_offset + size:
                return None
            data = self._buffer[self._read_offset : self._read_offset + size]
            self._read_offset += size
            return struct.unpack(fmt, data)[0]

    def read_list[
        T
    ](self, obj_type: type[T], num_bytes: int = None, signed: bool = True) -> list[T]:
        with self._lock:
            size = self.read_size()
            if size is None:
                return None
            result = []
            for _ in range(size):
                item = self.read(obj_type, num_bytes=num_bytes, signed=signed)
                if item is None:
                    return None
                result.append(item)
            return result

    def read_string(self):
        result = self.read_list(str)
        return (
            b"".join(c for c in result).decode("ascii") if result is not None else None
        )

    def _get_format_from_bytes(self, obj_type: type, num_bytes: int, signed: bool):
        if obj_type == int:
            if num_bytes is None:
                raise ValueError("Number of bytes must be provided")
            if signed:
                if num_bytes == 1:
                    return "<b"
                elif num_bytes == 2:
                    return "<h"
                elif num_bytes == 4:
                    return "<i"
                elif num_bytes == 8:
                    return "<q"
                else:
                    raise ValueError(f"Unsupported number of bytes: {num_bytes}")
            else:
                if num_bytes == 1:
                    return "<B"
                elif num_bytes == 2:
                    return "<H"
                elif num_bytes == 4:
                    return "<I"
                elif num_bytes == 8:
                    return "<Q"
                else:
                    raise ValueError(f"Unsupported number of bytes: {num_bytes}")
        elif obj_type == bool:
            return "<?"
        elif obj_type == float:
            if num_bytes is None:
                raise ValueError("Number of bytes must be provided")
            if num_bytes == 4:
                return "<f"
            elif num_bytes == 8:
                return "<d"
            else:
                raise ValueError(f"Unsupported number of bytes: {num_bytes}")
        elif obj_type == str:
            return "<c"
        else:
            raise ValueError(f"Unsupported object type: {obj_type}")

    def _grow_if_needed(self, write_length: int):
        final_length = self._write_offset + write_length
        resize_needed = len(self._buffer) <= final_length

        if resize_needed:
            self._buffer.extend(bytearray(final_length - len(self._buffer)))

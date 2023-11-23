from tiny_coin.binary_buffer import BinaryBuffer
from tiny_coin.generics import (
    bool8,
    int8,
    int16,
    int32,
    int64,
    uint8,
    uint16,
    uint32,
    uint64,
)
from tiny_coin.utils import list_to_type


def test_primitive_read_write():
    buffer = BinaryBuffer()

    b = bool8(True)
    buffer.write(b)
    b_read = buffer.read(bool8)
    assert b == b_read

    u8 = uint8(3)
    buffer.write(u8)
    u8_read = buffer.read(uint8)
    assert u8 == u8_read

    i8 = int8(-5)
    buffer.write(i8)
    i8_read = buffer.read(int8)
    assert i8 == i8_read

    u16 = uint16(10000)
    buffer.write(u16)
    u16_read = buffer.read(uint16)
    assert u16 == u16_read

    i16 = int16(-5000)
    buffer.write(i16)
    i16_read = buffer.read(int16)
    assert i16 == i16_read

    u32 = uint32(7000000)
    buffer.write(u32)
    u32_read = buffer.read(uint32)
    assert u32 == u32_read

    i32 = int32(-3000000)
    buffer.write(i32)
    i32_read = buffer.read(int32)
    assert i32 == i32_read

    u64 = uint64(4000000000)
    buffer.write(u64)
    u64_read = buffer.read(uint64)
    assert u64 == u64_read

    i64 = int64(-2000000000)
    buffer.write(i64)
    i64_read = buffer.read(int64)
    assert i64 == i64_read


def test_str_read_write():
    buffer = BinaryBuffer()

    actual = "foo"
    buffer.write(actual)
    read = buffer.read(str)
    assert actual == read


def test_list_read_write():
    buffer = BinaryBuffer()

    u8 = list_to_type([3, 5, 7, 9, 11, 55, 75], uint8)
    buffer.write(u8)
    u8_read = buffer.read(list[uint8])
    assert u8 == u8_read

    i8 = list_to_type([-6, -14, -32, -44, -65, -77, -99, -102], int8)
    buffer.write(i8)
    i8_read = buffer.read(list[int8])
    assert i8 == i8_read

    u16 = list_to_type([10000, 20000, 30000, 40000, 50000], uint16)
    buffer.write(u16)
    u16_read = buffer.read(list[uint16])
    assert u16 == u16_read

    i16 = list_to_type([-5000, -6000, -7000, -8000, -9000, -10000], int16)
    buffer.write(i16)
    i16_read = buffer.read(list[int16])
    assert i16 == i16_read

    u32 = list_to_type([7000000, 8000000, 9000000], uint32)
    buffer.write(u32)
    ui32_read = buffer.read(list[uint32])
    assert u32 == ui32_read

    i32 = list_to_type([-3000000, -4000000, -5000000], int32)
    buffer.write(i32)
    i32_read = buffer.read(list[int32])
    assert i32 == i32_read

    u64 = list_to_type([4000000000, 5000000000, 6000000000], uint64)
    buffer.write(u64)
    ui64_read = buffer.read(list[uint64])
    assert u64 == ui64_read

    i64 = list_to_type([-2000000000, -5000000000, -8000000000], int64)
    buffer.write(i64)
    i64_read = buffer.read(list[int64])
    assert i64 == i64_read

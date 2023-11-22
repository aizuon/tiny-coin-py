from src.binary_buffer import BinaryBuffer


def test_primitive_read_write():
    buffer = BinaryBuffer()

    b = True
    buffer.write(b)
    b_read = buffer.read(bool)
    assert b == b_read

    u8 = 3
    buffer.write(u8, 1, False)
    u8_read = buffer.read(int, 1, False)
    assert u8 == u8_read

    i8 = -5
    buffer.write(i8, 1, True)
    i8_read = buffer.read(int, 1, True)
    assert i8 == i8_read

    u16 = 10000
    buffer.write(u16, 2, False)
    u16_read = buffer.read(int, 2, False)
    assert u16 == u16_read

    i16 = -5000
    buffer.write(i16, 2, True)
    i16_read = buffer.read(int, 2, True)
    assert i16 == i16_read

    u32 = 7000000
    buffer.write(u32, 4, False)
    u32_read = buffer.read(int, 4, False)
    assert u32 == u32_read

    i32 = -3000000
    buffer.write(i32, 4, True)
    i32_read = buffer.read(int, 4, True)
    assert i32 == i32_read

    u64 = 4000000000
    buffer.write(u64, 8, False)
    u64_read = buffer.read(int, 8, False)
    assert u64 == u64_read

    i64 = -2000000000
    buffer.write(i64, 8, True)
    i64_read = buffer.read(int, 8, True)
    assert i64 == i64_read


def test_str_read_write():
    buffer = BinaryBuffer()

    actual = "foo"
    buffer.write_string(actual)
    read = buffer.read_string()
    assert actual == read


def test_list_read_write():
    buffer = BinaryBuffer()

    u8 = [3, 5, 7, 9, 11, 55, 75]
    buffer.write_list(u8, 1, False)
    u8_read = buffer.read_list(int, 1, False)
    assert u8 == u8_read

    i8 = [-6, -14, -32, -44, -65, -77, -99, -102]
    buffer.write_list(i8, 1, True)
    i8_read = buffer.read_list(int, 1, True)
    assert i8 == i8_read

    u16 = [10000, 20000, 30000, 40000, 50000]
    buffer.write_list(u16, 2, False)
    u16_read = buffer.read_list(int, 2, False)
    assert u16 == u16_read

    i16 = [-5000, -6000, -7000, -8000, -9000, -10000]
    buffer.write_list(i16, 2, True)
    i16_read = buffer.read_list(int, 2, True)
    assert i16 == i16_read

    ui32 = [7000000, 8000000, 9000000]
    buffer.write_list(ui32, 4, False)
    ui32_read = buffer.read_list(int, 4, False)
    assert ui32 == ui32_read

    i32 = [-3000000, -4000000, -5000000]
    buffer.write_list(i32, 4, True)
    i32_read = buffer.read_list(int, 4, True)
    assert i32 == i32_read

    ui64 = [4000000000, 5000000000, 6000000000]
    buffer.write_list(ui64, 8, False)
    ui64_read = buffer.read_list(int, 8, False)
    assert ui64 == ui64_read

    i64 = [-2000000000, -5000000000, -8000000000]
    buffer.write_list(i64, 8, True)
    i64_read = buffer.read_list(int, 8, True)
    assert i64 == i64_read

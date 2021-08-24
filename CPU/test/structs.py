from ctypes import POINTER, Structure, c_int16, c_int8, c_size_t, c_uint64, c_uint8, c_uint16, cdll

instruction_t = c_int16
byte_t = c_int8
bit_t = c_uint8
addr_t = c_uint16


NUM_REGISTER = 32
SIZE_IO = 64
SIZE_EXT_IO = 160


class memory_t (Structure):
    _fields_ = [
        ("sram_size", c_size_t),
        ("flash_size", c_size_t),
        ("sram", POINTER(byte_t)),
        ("flash", POINTER(instruction_t))
    ]


class sreg_t (Structure):
    _fields_ = [
        ("C", bit_t),
        ("Z", bit_t),
        ("N", bit_t),
        ("V", bit_t),
        ("S", bit_t),
        ("H", bit_t),
        ("T", bit_t),
        ("I", bit_t),
    ]


class cpu_t (Structure):
    _fields_ = [
        ("r", c_int8 * NUM_REGISTER),
        ("sreg", POINTER(sreg_t)),
        ("io", byte_t * SIZE_IO),
        ("ext_io", byte_t * SIZE_EXT_IO),
        ("memory", POINTER(memory_t)),
        ("PC", addr_t),
        ("clock_cycles", c_uint64)
    ]

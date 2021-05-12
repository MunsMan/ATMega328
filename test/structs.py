from ctypes import *


class gpr_t (Structure):
    _fields_ = [
        ("r", POINTER(c_uint8)),
        ("size", c_uint8),
        ("X", c_uint8),
        ("Y", c_uint8),
        ("Z", c_uint8)
    ]


class SRAM(Structure):
    _fields_ = [
        ("grp", POINTER(gpr_t)),
        ("io", POINTER(c_uint8)),
        ("extIO", POINTER(c_uint8)),
        ("sram", POINTER(c_uint8))
    ]


class EEPROM(Structure):
    _fields_ = [
        ("eeprom", POINTER(c_uint8)),
        ("write_ops", c_uint)
    ]


class MEM (Structure):
    _fields_ = [
        ("flash", POINTER(c_uint16)),
        ("sram", POINTER(SRAM)),
        ("eeprom", POINTER(EEPROM))
    ]


class sr_t (Structure):
    _fields_ = [
        ("I", c_uint8, 1),
        ("T", c_uint8, 1),
        ("H", c_uint8, 1),
        ("S", c_uint8, 1),
        ("V", c_uint8, 1),
        ("N", c_uint8, 1),
        ("Z", c_uint8, 1),
        ("C", c_uint8, 1)
    ]


class cpu_t (Structure):
    _fields_ = [
        ("SP", c_uint16),
        ("PC", c_uint16),
        ("gpr", POINTER(gpr_t)),
        ("mem", POINTER(MEM)),
        ("sr", POINTER(sr_t))
    ]


testlib = cdll.LoadLibrary('bin/test.so')
testlib.initCPU.restype = POINTER(cpu_t)
testlib.getSR.restype = POINTER(sr_t)

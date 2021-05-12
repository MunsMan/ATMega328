from ctypes import *
from structs import cpu_t, sr_t, testlib


def _add_flags(sr, Rd: c_int8, Rr: c_int8):
    testlib.resetSR(sr)
    Rd7 = Rd.value >> 7 & 1
    Rr7 = Rr.value >> 7 & 1

    solution = c_int8(Rd.value + Rr.value)
    res = c_int8(testlib._add(sr, Rd, Rr)).value
    R7 = res >> 7 & 1
    if solution.value != res:
        assert solution.value == res

    if testlib.getVFlag(sr):  # Two complement overflow indicator
        assert (Rd7 & Rr7 & ~R7) | (~Rd7 & ~Rr7 & R7)

    assert testlib.getNFlag(sr) == R7
    assert testlib.getSFlag(sr) == testlib.getNFlag(sr) ^ testlib.getVFlag(sr)
    assert testlib.getZFlag(sr) == (res == 0)
    assert testlib.getCFlag(sr) == Rd7 & Rr7 | Rr7 & ~R7 | ~R7 & Rd7


def _adc_flags(sr, Rd: c_int8, Rr: c_int8):
    testlib.resetSR(sr)
    testlib.setCFlag(sr, 1)
    Rd7 = Rd.value >> 7 & 1
    Rr7 = Rr.value >> 7 & 1

    solution = c_int8(Rd.value + Rr.value + 1)
    res = c_int8(testlib._add(sr, Rd, Rr)).value
    R7 = res >> 7 & 1
    if solution.value != res:
        assert solution.value == res

    assert testlib.getVFlag(sr) == (Rd7 & Rr7 & ~R7) | (~Rd7 & ~Rr7 & R7)
    assert testlib.getNFlag(sr) == R7
    assert testlib.getSFlag(sr) == testlib.getNFlag(sr) ^ testlib.getVFlag(sr)
    assert testlib.getZFlag(sr) == (res == 0)
    assert testlib.getCFlag(sr) == Rd7 & Rr7 | Rr7 & ~R7 | ~R7 & Rd7


def _adiw_flags(sr, Rd: c_int16, K: c_int8) -> None:
    testlib.resetSR(sr)
    S: c_int16 = c_int16(Rd.value + K.value).value
    R: c_int16 = c_int16(testlib._adiw(sr, Rd, K)).value
    Rdh7: bool = Rd.value >> 15 & 1
    S15: bool = S >> 15 & 1
    R15: bool = R >> 15 & 1
    assert S == R
    assert S15 == R15
    assert testlib.getVFlag(sr) == ~Rdh7 & R15
    assert testlib.getNFlag(sr) == R15
    assert testlib.getSFlag(sr) == testlib.getNFlag(sr) ^ testlib.getVFlag(sr)
    assert testlib.getZFlag(sr) == (R == 0)
    assert testlib.getCFlag(sr) == ~R15 & Rdh7


def _and_flags(sr, Rd: c_int8, Rr: c_int8) -> None:
    testlib.resetSR(sr)
    expected = c_uint8(Rd.value & Rr.value).value
    result = c_uint8(testlib._and(sr, Rd, Rr)).value
    R7 = expected >> 7
    assert expected == result
    assert testlib.getSFlag(sr) == R7 ^ 0
    assert testlib.getVFlag(sr) == 0
    assert testlib.getNFlag(sr) == R7
    assert testlib.getZFlag(sr) == (expected == 0)

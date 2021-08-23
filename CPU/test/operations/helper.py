def twoOp(upcode: int, rd: int, rr: int) -> int:
    return upcode + (rd << 4) + (rr & (1 << 5)) + (rr & 0xF)

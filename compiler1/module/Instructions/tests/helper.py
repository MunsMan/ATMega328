def mock_exit(*_): return exit()


def getAllRegisterPointer():
    full = map(lambda x: 'r' + str(x) + ":r" + str(x+1), range(0, 31))
    half = map(lambda x: 'r' + str(x) + ":", range(0, 31))
    pointer = ['X', 'Y', 'Z']
    return list(full) + list(half) + pointer


def getBitAt(byte: int, index: int):
    return (byte & 1 << index - 1) >> (index - 1)


def fromBitMask(mask: str, **kwargs: int):
    charDict = {}
    mask = mask.replace(" ", "")
    mask = mask.replace("_", "")
    for bit in mask:
        if not bit.isdigit():
            if bit in charDict:
                charDict[bit] += 1
            else:
                charDict[bit] = 1
    for bit in mask:
        if not bit.isdigit():
            value = getBitAt(kwargs[bit], charDict[bit])
            charDict[bit] -= 1
            mask = mask.replace(bit, str(value), 1)
    return int(mask, 2)

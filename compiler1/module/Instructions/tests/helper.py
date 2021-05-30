def mock_exit(*_): return exit()


def getAllRegisterPointer():
    full = map(lambda x: 'r' + str(x) + ":r" + str(x+1), range(0, 31))
    half = map(lambda x: 'r' + str(x) + ":", range(0, 31))
    pointer = ['X', 'Y', 'Z']
    return list(full) + list(half) + pointer

from .helper import bit3, bit7


def test_bit3():
    for i in range(0, 8):
        number = 1 << i
        if i != 3:
            assert bit3(number) == False
        else:
            assert bit3(number) == True


def test_bit7():
    for i in range(0, 8):
        number = 1 << i
        if i != 7:
            assert bit7(number) == False
        else:
            assert bit7(number) == True

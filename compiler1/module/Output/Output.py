from typing import List


class Output:
    def __init__(self, parseCode: List[int]) -> None:
        self.parseCode: List[int] = parseCode

    def bin(self, filename: str = "a.bin") -> None:
        with open(filename, "w") as file:
            for line in self.parseCode:
                file.write(self.toBin(line))

    @staticmethod
    def toBin(opcode: int) -> str:
        lenInstruction = 16 if opcode.bit_length() <= 16 else 32
        instrcution = bin(opcode)[2:]
        return "0" * (lenInstruction - len(instrcution)) + instrcution

    def hex(self, filename: str = "a.hex") -> None:
        with open(filename, "w") as file:
            for line in self.parseCode:
                file.write("0x%04X\n" % line)

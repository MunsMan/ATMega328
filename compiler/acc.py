#!/usr/bin/python3

from typing import Iterator, List, Tuple
from instructions import instructionMapping
import struct
import sys
from error import throwError, LineRev


def sourceCodeGenerator(file: str) -> Iterator[Tuple[int, str]]:
    lines: List[str] = []
    try:
        with open(file) as fd:
            lines = fd.readlines()
    except(OSError, IOError) as e:
        throwError(2, False,  (file, e))

    nLine = 0
    for line in lines:
        nLine += 1
        # filter for comments
        if line.find("//") != -1:
            line = line[0:line.find("//")]
        if line.replace("\n", "").replace(" ", "") == "":
            continue
        yield (nLine, line.strip())


def parseLine(line: str) -> Tuple[str, str, str, str, str, str]:

    line: List[str] = line.split(" ")

    op: str = line[0][0:4]
    cond: str = ""
    flags: str = ""

    Rd: str = (line[1] if len(line) >= 2 else "")
    Rn: str = (line[2] if len(line) >= 3 else "")
    op2: str = (line[3] if len(line) >= 4 else "")

    if len(line[0]) >= 5:
        cond: str = line[0][3:5]
    if len(line[0]) == 4:
        flag = line[0][3]
    elif len(line[0]) == 6:
        flag = line[0][6]

    return (op, cond, flags, Rd, Rn, op2)


def compileOp(args: Tuple[str, str, str, str, str, str]) -> int:
    op, cond, flags, Rd, Rn, op2 = args
    return instructionMapping(op.upper())(cond, flags, Rd, Rn, op2)


def printAsHex(bs: List[int]) -> None:
    for b in bs:
        print(format(b, "X"))


def asBin(bs: List[int], fileName: str) -> None:
    f = open(fileName, "w")
    s: str = ""
    for b in bs:
        s += ascii(format(b, "b").zfill(16)).replace("'", "")
    f.write(s)
    f.close()


def main():
    if len(sys.argv) < 2:
        throwError(1, False)

    filePath: str = sys.argv[1]
    lines: List[int] = []
    for nLine, line in sourceCodeGenerator(filePath):
        LineRev.setLine(nLine, line)
        lines.append(compileOp(parseLine(line)))
    printAsHex(lines)
    outputFileName = filePath
    if outputFileName.find(".") != -1:
        outputFileName = outputFileName[0:outputFileName.find(".")] + ".out"
    asBin(lines, outputFileName)


if __name__ == "__main__":
    main()

#!/usr/bin/python3
from typing import List
import sys
from module import FileReader, throwError, LabelDecoder, Parser


def main():
    if len(sys.argv) < 2:
        throwError(1, False)
    filepath = sys.argv[1]
    fileReader = FileReader(filepath)
    labelDecoder = LabelDecoder(fileReader.lines)
    parser = Parser(labelDecoder.labelRef)
    labelDecoder.printLabels()
    res = parser.parseLabels(labelDecoder.labels)
    labelDecoder.parsedLabels = res
    for label in res:
        print(label)
        _, instructions = res[label]
        for _, instruction in instructions:
            for inst in instruction():
                print("\t0x%04X" % inst)


if __name__ == "__main__":
    main()

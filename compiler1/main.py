#!/usr/bin/python3
import sys
from module import FileReader, throwError, LabelDecoder, Parser


def main():
    if len(sys.argv) < 2:
        throwError(1, False)
    filepath = sys.argv[1]
    fileReader = FileReader(filepath)
    labelDecoder = LabelDecoder(fileReader.lines)
    parsedLabels = Parser(labelDecoder.labels, labelDecoder.labelRef).parse()
    labelDecoder.parsedLabels = parsedLabels
    for label in parsedLabels:
        print(label)
        _, instructions = parsedLabels[label]
        for _, instruction in instructions:
            for inst in instruction():
                print("\t0x%04X" % inst)


if __name__ == "__main__":
    main()

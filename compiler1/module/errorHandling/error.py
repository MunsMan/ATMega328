from typing import Dict, Tuple, Any, Callable
from . import LineRev


def throwError(errorCode: int, line: bool, custom: Any = None):
    customError = errorCodeMap[errorCode]
    customErrorMessage: str = customError(custom)
    errorWrapper(errorCode, line,  customErrorMessage)


def errorWrapper(errorCode: int, line: bool,  customMessage: str):
    if line:
        print("Error:\nLine " + LineRev.getNumLine() +
              ": " + LineRev.getLine() + "\n" + customMessage)
    else:
        print(customMessage)
    exit(errorCode)


def missingInputFile(custom: None) -> str:
    return "Please specify an input file!\nUsually it is a '.asm' file"


def failedLoadingInputFile(custom: Tuple[str, str]) -> str:
    fileName, error = custom
    return "Failed to load the provided file: " + fileName + "\nPython Error:\n" + repr(error)


def undefindeArgument(custom: Tuple[str, str, int]) -> str:
    R, eType, eSize = custom
    return "Can't parse following Argument: " + R + "\nExpected " + eType + " of Size: " + str(eSize)


def wrongArgumentRegister(custom: Tuple[str, int, str, int, str]) -> str:
    R, expectedSize, expectedType, passedSize, passedType = custom
    if passedSize == -1:
        return undefindeArgument((R, expectedType, expectedSize))
    return "Register " + R + " only takes Argument of size: " + str(expectedSize) + " " + expectedType + " but you provided Argument of Size " + str(passedSize) + " " + passedType


def unknownInstructionError(custom: Any) -> str:
    op = custom
    return "Compiler Error:\nCan't parse following instruction: '{op}'\nPlease reference to the Documentation for available Instructions. ".format(op=op)


def invalidRegisterReference(custom: str) -> str:
    r: str = custom
    return "Invalid Register:\nThe used Register is not definde for that Processor. Please check the passed Register: {r}.\nValid Register are in range of r0-r31.".format(r=r)


def invalidConstantError(custom: str) -> str:
    n = custom
    return "Passed Constant can't be interpreted as valid Number.\n Please ensure that it is a number: {n}\n".format(n=n)


def wrongArgumentConstant(custom: Tuple[int, int]) -> str:
    constant, constant_size, argSize = custom
    return "A Constant can only take an Argument of size: {ks} Bit.\nYou provided a Constant: {K}\nIt is of Size {aS} Bit.".format(K=constant, ks=constant_size, aS=argSize)


def wrongRegisterReferenced(custom: Tuple[str, str]) -> str:
    passedRegister, supportedRegisters = custom
    return "You passed Register {pR}.\nOnly following Registers are Supported:\n{sPs}".format(pR=passedRegister, sPs=supportedRegisters)


def invalidCondError(custom: Tuple[str]) -> str:
    cond = custom
    return "Invalid condition used: {cond}\nThis condition is not supported. Please reference to the instruction Set Manual".format(cond=cond)


errorCodeMap: Dict[int, Callable[[Any], str]] = {
    1: missingInputFile,
    2: failedLoadingInputFile,
    3: wrongArgumentRegister,
    4: unknownInstructionError,
    5: invalidRegisterReference,
    6: invalidConstantError,
    7: wrongArgumentConstant,
    8: wrongRegisterReferenced,
    9: invalidCondError,
}

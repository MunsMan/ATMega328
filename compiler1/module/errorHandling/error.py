from typing import Dict, Tuple, Any, Callable
from .LineRef import LineRef


def throwError(errorCode: int, line: bool, custom: Any = None):
    customError = errorCodeMap[errorCode]
    customErrorMessage: str = customError(custom)
    errorWrapper(errorCode, line,  customErrorMessage)


def errorWrapper(errorCode: int, line: bool,  customMessage: str):
    if line:
        print("Error:\nLine " + LineRef.getNumLine() +
              ": " + LineRef.getLine() + "\n" + customMessage)
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


def invalidImmediateError(custom: str) -> str:
    n = custom
    return "Passed Immediate can't be interpreted as valid unsigned Integer.\n Please ensure that it is a number: {n}\n".format(n=n)


def wrongImmediateSize(custom: Tuple[int, int, int]) -> str:
    immediate, immediate_size, expected_size = custom
    return "An Immediate can only take an Argument of size: {ks} Bit.\nYou provided this Immediate: {K}\nIt is of size {aS} Bit.\n".format(K=immediate, ks=immediate_size, aS=expected_size)


def wrongRegisterReferenced(custom: Tuple[str, str]) -> str:
    passedRegister, supportedRegisters = custom
    return "You passed Register {pR}.\nOnly following Registers are Supported:\n{sPs}".format(pR=passedRegister, sPs=supportedRegisters)


def invalidCondError(custom: Tuple[str]) -> str:
    cond = custom
    return "Invalid condition used: {cond}\nThis condition is not supported. Please reference to the instruction Set Manual".format(cond=cond)


def wrongTwoComplementSize(custom: Tuple[str]) -> str:
    immediate, expected_size = custom
    sign = "negativ"
    if immediate >= 0:
        sign = "positiv"
        expected_size -= 1
    diff = immediate.bit_length() - (expected_size-1)
    return "A {sign} Immediate in the Two's Complement can only be of size: {pos_size}bit.\nYou provided an Immediate of size: {immediate_size}bit.\nThat is {diff}bit to long.\n".format(pos_size=expected_size-1, immediate_size=immediate.bit_length(), diff=diff, sign=sign)


def wrongRegisterPointer(custom) -> str:
    reg_p, lowest, even = custom
    if even:
        even = "For this Operation, only even RegisterPointer are allowed.\n"
    return "Wrong use of RegisterPointer.\nRegister Pointer should be higer or equal then {lowest} and smaller then 32.\n{even}You passed the follwing: {reg_p}".format(lowest=lowest, reg_p=reg_p, even=even)


def invalidRegisterReference(custom) -> str:
    reg_p = custom
    return "Invalid Register Pointer.\nYou provided the following Register Pointer: {reg_p}.\nIt couldn't be parsed or is not defined for this CPU.\n Please check the docs for more information.\n".format(reg_p=reg_p)


def wrongArgumentError(custom) -> str:
    opcode, argument = custom
    return f"Argument can't be paired with the opcode.\nOpcode: {opcode}\nArgument: {argument}\nPlease use Documentation for reference.\n"


errorCodeMap: Dict[int, Callable[[Any], str]] = {
    1: missingInputFile,
    2: failedLoadingInputFile,
    3: wrongArgumentRegister,
    4: unknownInstructionError,
    5: invalidRegisterReference,
    6: invalidImmediateError,
    7: wrongImmediateSize,
    8: wrongRegisterReferenced,
    9: invalidCondError,
    10: wrongTwoComplementSize,
    11: wrongRegisterPointer,
    12: invalidRegisterReference,
    13: wrongArgumentError,
}

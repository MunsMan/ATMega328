class LineRef():
    __nLine = 0
    __line = ""

    @staticmethod
    def setLine(newNLine: int, newLine: str) -> None:
        LineRef.__nLine = newNLine
        LineRef.__line = newLine

    @staticmethod
    def getLine() -> str:
        return LineRef.__line

    @staticmethod
    def getNumLine() -> str:
        return str(LineRef.__nLine)

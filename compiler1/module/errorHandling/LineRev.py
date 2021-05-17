class LineRev():
    def __init__(self):
        LineRev.__nLine = 0
        LineRev.__line = ""

    @staticmethod
    def setLine(newNLine: int, newLine: str) -> None:
        LineRev.__nLine = newNLine
        LineRev.__line = newLine

    @staticmethod
    def getLine() -> str:
        return LineRev.__line

    @staticmethod
    def getNumLine() -> str:
        return str(LineRev.__nLine)

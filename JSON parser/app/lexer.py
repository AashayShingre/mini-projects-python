from app.tokentypes import tokenType, Token
import re


class Lexer:
    seek: int
    jsonStr: str
    tokens: list
    n: int

    def __init__(self, jsonStr: str):
        self.seek = 0
        self.jsonStr = jsonStr
        self.tokens = []
        self.n = len(jsonStr)
        self.getTokens()

    def getTokens(self) -> list[Token]:
        while self.seek < self.n:
            match self.jsonStr[self.seek]:
                case (
                    " " | "\n"
                ):  # would have to do "\r\n" or "\r" if you're not using universal newline mode while reading file.
                    self.seek += 1
                case "{":
                    self.tokens.append((tokenType.LEFT_CURL,))
                    self.seek += 1
                case "}":
                    self.tokens.append((tokenType.RIGHT_CURL,))
                    self.seek += 1
                case "[":
                    self.tokens.append((tokenType.LEFT_SQUARE,))
                    self.seek += 1
                case "]":
                    self.tokens.append((tokenType.RIGHT_SQUARE,))
                    self.seek += 1
                case ":":
                    self.tokens.append((tokenType.COLON,))
                    self.seek += 1
                case ",":
                    self.tokens.append((tokenType.COMMA,))
                    self.seek += 1
                case '"':
                    self.addString()
                case "n":
                    self.addNull()
                case "t":
                    self.addBool("true")
                case "f":
                    self.addBool("false")
                case _:
                    self.addNumber()
        return self.tokens

    def addString(self):
        tempSeek = self.seek + 1
        while tempSeek < self.n and self.jsonStr[tempSeek] != '"':
            tempSeek += 1
        self.tokens.append((tokenType.STRING, self.jsonStr[self.seek + 1 : tempSeek]))
        self.seek = tempSeek + 1

    def addNumber(self):
        # allowed json numbers are - 42, 42.0, 4.2E+1
        validNumChars = r"[0-9\-\+eE\.]"  # I'll just save me some misery here

        # the first character is expected to be number
        if not re.match(validNumChars, c := self.jsonStr[self.seek]):
            self.raiseInvalid()

        tempSeek = self.seek + 1
        # keep looping till will see valid chars
        while tempSeek < self.n and re.match(r"[0-9\-\+eE\.]", self.jsonStr[tempSeek]):
            tempSeek += 1

        numStr = self.jsonStr[self.seek : tempSeek]

        # verify if valid number is obtained
        json_number_pattern = r"^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$"
        if re.match(json_number_pattern, numStr):
            try:
                self.tokens.append((tokenType.NUMBER, int(numStr)))
            except ValueError:
                self.tokens.append((tokenType.NUMBER, float(numStr)))
            except:
                self.raiseInvalid()
        else:
            self.raiseInvalid()

        self.seek = tempSeek

    def addNull(self):
        if self.jsonStr[self.seek : self.seek + 4] == "null":
            self.tokens.append((tokenType.NULL, None))
            self.seek += 4
        else:
            self.raiseInvalid()

    def addBool(self, boolVal):
        if self.jsonStr[self.seek : self.seek + len(boolVal)] == boolVal:
            self.tokens.append((tokenType.BOOLEAN, boolVal == "true"))
            self.seek += len(boolVal)
        else:
            self.raiseInvalid()

    def raiseInvalid(self):
        raise ValueError(
            f"Invalid token starting with {self.jsonStr[self.seek]} at -> {self.jsonStr[self.seek:self.seek+10]}"
        )


def getTokens(jsonStr: str) -> list[Token]:
    lexer = Lexer(jsonStr)
    return lexer.tokens

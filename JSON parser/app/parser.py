from typing import Any
from app.tokentypes import tokenType, Token


class Parser:
    seek: int
    tokens: list[Token]
    n: int
    result: dict[str, Any]

    def __init__(self, tokens: list[Token]):
        self.seek = 0
        self.tokens = tokens
        self.n = len(tokens)
        self.result = self.parse()

    def parse(self):
        # expect the first token to be '{', which then builds a dictionary
        self.seek = 0
        if self.n > 0 and self.tokens[self.seek][0] == tokenType.LEFT_CURL:
            self.seek += 1
            return self.getObject()
        else:
            self.raiseInvalid("JSON starts with { ")

    def getObject(self):
        if self.tokens[self.seek][0] == tokenType.RIGHT_CURL:
            self.seek += 1
            return {}

        resultObject = {}
        while self.seek < self.n:
            key = self.getKey()

            if self.seek >= self.n:
                self.raiseInvalid("colon(:) expected, found EOF")
            elif (t := self.tokens[self.seek][0]) != tokenType.COLON:
                self.raiseInvalid(f"colon(:) expected at {self.seek} ({t})")
            else:
                self.seek += 1

            value = self.getValue()

            resultObject[key] = value

            if (c := self.tokens[self.seek][0]) == tokenType.COMMA:
                self.seek += 1
            elif c == tokenType.RIGHT_CURL:
                self.seek += 1
                return resultObject
            else:
                self.raiseInvalid(
                    f"Unexpected token at {self.seek} ({c}). ',' or {'}'} expected"
                )

        self.raiseInvalid(f"Incomplete Obj at {self.seek}")

    def getKey(self):
        if self.seek < self.n and self.tokens[self.seek][0] == tokenType.STRING:
            val = self.tokens[self.seek][1]
            self.seek += 1
            return val
        elif self.seek >= self.n:
            self.raiseInvalid(f"String expected, got EOF")
        else:
            self.raiseInvalid(f"String expected, got {self.tokens[self.seek]}")

    def getValue(self):
        if self.seek >= self.n:
            self.raiseInvalid(f"Expected value, got EOF")

        match self.tokens[self.seek]:
            case (
                tokenType.STRING
                | tokenType.NUMBER
                | tokenType.BOOLEAN
                | tokenType.NULL,
                val,
            ):
                self.seek += 1
                return val
            case (tokenType.LEFT_CURL,):
                self.seek += 1
                return self.getObject()
            case (tokenType.LEFT_SQUARE,):
                self.seek += 1
                return self.getArray()
            case _:
                self.raiseInvalid(f"Unexpected token {self.tokens[self.seek]}")

    def getArray(self):
        if self.tokens[self.seek][0] == tokenType.RIGHT_SQUARE:
            self.seek += 1
            return []

        resultArr = []
        while self.seek < self.n:
            resultArr.append(self.getValue())

            if (c := self.tokens[self.seek][0]) == tokenType.COMMA:
                self.seek += 1
            elif c == tokenType.RIGHT_SQUARE:
                self.seek += 1
                return resultArr
            else:
                self.raiseInvalid(
                    f"Unexpected token at {self.seek} ({c}). , or {']'} expected"
                )

    def raiseInvalid(self, message):
        raise ValueError(f"Invalid structure - {message}")


def parseTokens(tokens: list[Token]) -> dict[str, Any]:
    parser = Parser(tokens)
    return parser.result

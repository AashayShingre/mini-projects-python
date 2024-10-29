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
                case ' ' | '\n':
                    pass
                case '{': 
                    self.tokens.append((tokenType.LEFT_CURL, ))
                case '}': 
                    self.tokens.append((tokenType.RIGHT_CURL, )) 
                case '[': 
                    self.tokens.append((tokenType.LEFT_SQUARE, ))
                case ']': 
                    self.tokens.append((tokenType.RIGHT_SQUARE, )) 
                case ':': 
                    self.tokens.append((tokenType.COLON,))
                case ',': 
                    self.tokens.append((tokenType.COMMA, )) 
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
            self.seek += 1
        return self.tokens

    def addString(self): 
        s = ''
        while self.seek + 1 < self.n and (c := self.jsonStr[self.seek + 1]) != '"':
            s += c
            self.seek += 1
        self.seek += 1
        self.tokens.append((tokenType.STRING, s))

    def addNumber(self):
        # I'll just save me some misery here
        validNumChars = r'[0-9\-\+eE\.]' 
        numStr = ''
        
        if re.match(validNumChars, c := self.jsonStr[self.seek]): 
            numStr += c
        else:
            self.raiseInvalid()

        while self.seek + 1 < self.n and re.match(r'[0-9\-\+eE\.]', c := self.jsonStr[self.seek + 1]): 
            numStr += c 
            self.seek += 1
        
        json_number_pattern = r'^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$'

        if re.match(json_number_pattern, numStr):
            try: 
                self.tokens.append((tokenType.NUMBER, int(numStr)))
            except ValueError: 
                self.tokens.append((tokenType.NUMBER, float(numStr)))
            except: 
                self.raiseInvalid()
        else: 
            self.raiseInvalid()


    def addNull(self):
        if self.jsonStr[self.seek:self.seek+4] == 'null': 
            self.tokens.append((tokenType.NULL, None))
            self.seek += 3
        else:
            self.raiseInvalid()

    def addBool(self, boolVal):
        if self.jsonStr[self.seek:self.seek+len(boolVal)] == boolVal: 
            self.tokens.append((tokenType.BOOLEAN, boolVal == 'true'))
            self.seek += len(boolVal) - 1
        else:
            self.raiseInvalid()

    def raiseInvalid(self): 
        raise ValueError(f"Invalid token starting with {self.jsonStr[self.seek]} at -> {self.jsonStr[self.seek:self.seek+10]}")

def getTokens(jsonStr : str) -> list[Token]: 
    lexer = Lexer(jsonStr)
    return lexer.tokens
import sys
from app.lexer import getTokens
from app.parser import parseTokens


def readAndParse():
    if len(sys.argv) < 2:
        raise ValueError("Missing argument: pass JSON file path as argument")
    for filePath in sys.argv[1:]:
        with open(filePath) as f:
            jsonStr = (
                f.read()
                .rstrip()
                .replace("\n", "")
                .replace(
                    "\r", ""
                )  # for older text formats, \r or \r\n also represents a newline
            )

            # jsonStr = json.loads(jsonStr) # LOL
            print(jsonLoads(jsonStr))


def jsonLoads(jsonStr: str) -> dict[str, str]:
    tokens = getTokens(jsonStr)
    return parseTokens(tokens)


if __name__ == "__main__":
    readAndParse()

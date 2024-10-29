from enum import Enum
from typing import Union, Optional

tokenType = Enum('tokenType', ['NUMBER', 'STRING', 'BOOLEAN', 'NULL', 'LEFT_CURL', 'RIGHT_CURL', 'LEFT_SQUARE', 'RIGHT_SQUARE', 'COLON', 'COMMA'])

Token = tuple[tokenType, Optional[Union[str, int, float]]]
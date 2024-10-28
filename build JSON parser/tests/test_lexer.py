from app.lexer import getTokens 
from app.tokentypes import tokenType
import pytest

def test_getTokens_brackets(): 
    assert getTokens('{ } ') == [(tokenType.LEFT_CURL, ), (tokenType.RIGHT_CURL, )]

def test_getTokens_string(): 
    assert getTokens('{"hello"') == [(tokenType.LEFT_CURL, ), (tokenType.STRING, "hello")]

def test_getTokens_all():
    assert getTokens('  {"hello" 0.23 1e5 } 5E6 {{null[true, false]') == [(tokenType.LEFT_CURL, ), (tokenType.STRING, "hello"), (tokenType.NUMBER, 0.23), (tokenType.NUMBER, 1e5), (tokenType.RIGHT_CURL, ), (tokenType.NUMBER, 5e6), (tokenType.LEFT_CURL, ), (tokenType.LEFT_CURL, ), (tokenType.NULL, None), (tokenType.LEFT_SQUARE, ), (tokenType.BOOLEAN, True), (tokenType.COMMA, ), (tokenType.BOOLEAN, False), (tokenType.RIGHT_SQUARE, )]

def test_getTokens_invalid_numbers1(): 
    with pytest.raises(ValueError):
        getTokens('0.a43') 

def test_getTokens_invalid_number2(): 
    with pytest.raises(ValueError):
        getTokens('03')       
        
def test_getTokens_invalid_numbers3(): 
    with pytest.raises(ValueError):
        getTokens('3.e4') 

def test_getTokens_invalid_numbers4(): 
    with pytest.raises(ValueError):
        getTokens('.3e4') 

def test_getTokens_invalid_numbers5(): 
    with pytest.raises(ValueError):
        getTokens('-2.2.2') 

def test_getTokens_invalid_token1(): 
    with pytest.raises(ValueError): 
        getTokens('nullt') 

def test_getTokens_invalid_bool(): 
    with pytest.raises(ValueError): 
        getTokens('True')
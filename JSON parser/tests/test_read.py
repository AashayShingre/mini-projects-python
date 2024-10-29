from app.read import jsonLoads
import pytest
import os 
import sys

def test_read_and_parse_step1_invalid(): 
    with pytest.raises(ValueError): 
        file_path = os.path.join(sys.path[0], 'tests', 'step1', 'invalid.json')
        with open(file_path) as f: 
            jsonStr = f.read()
            jsonLoads(jsonStr)

def test_read_and_parse_step1_valid(): 
    file_path = os.path.join(sys.path[0], 'tests', 'step1', 'valid.json')
    with open(file_path) as f: 
        jsonStr = f.read()
        assert jsonLoads(jsonStr) == {} 

def test_read_and_parse_step2_invalid(): 
    with pytest.raises(ValueError): 
        file_path = os.path.join(sys.path[0], 'tests', 'step2', 'invalid.json')
        with open(file_path) as f: 
            jsonStr = f.read()
            jsonLoads(jsonStr)

def test_read_and_parse_step2_invalid2(): 
    with pytest.raises(ValueError): 
        file_path = os.path.join(sys.path[0], 'tests', 'step2', 'invalid2.json')
        with open(file_path) as f: 
            jsonStr = f.read()
            jsonLoads(jsonStr)

def test_read_and_parse_step2_valid(): 
    file_path = os.path.join(sys.path[0], 'tests', 'step2', 'valid.json')
    with open(file_path) as f: 
        jsonStr = f.read()
        assert jsonLoads(jsonStr) == {"key": "value"}

def test_read_and_parse_step2_valid2(): 
    file_path = os.path.join(sys.path[0], 'tests', 'step2', 'valid2.json')
    with open(file_path) as f: 
        jsonStr = f.read()
        assert jsonLoads(jsonStr) == {"key": "value", "key2": "value"}


def test_read_and_parse_step3_invalid(): 
    with pytest.raises(ValueError): 
        file_path = os.path.join(sys.path[0], 'tests', 'step3', 'invalid.json')
        with open(file_path) as f: 
            jsonStr = f.read()
            jsonLoads(jsonStr)

def test_read_and_parse_step3_valid(): 
    file_path = os.path.join(sys.path[0], 'tests', 'step3', 'valid.json')
    with open(file_path) as f: 
        jsonStr = f.read()
        assert jsonLoads(jsonStr) == {"key1": True, "key2": False, "key3": None, "key4": "value", "key5": 101}

def test_read_and_parse_step4_invalid(): 
    with pytest.raises(ValueError): 
        file_path = os.path.join(sys.path[0], 'tests', 'step4', 'invalid.json')
        with open(file_path) as f: 
            jsonStr = f.read()
            jsonLoads(jsonStr)

def test_read_and_parse_step4_valid(): 
    file_path = os.path.join(sys.path[0], 'tests', 'step4', 'valid.json')
    with open(file_path) as f: 
        jsonStr = f.read()
        assert jsonLoads(jsonStr) == {"key": "value", "key-n": 101, "key-o": {}, "key-l": []}

def test_read_and_parse_step4_valid2(): 
    file_path = os.path.join(sys.path[0], 'tests', 'step4', 'valid2.json')
    with open(file_path) as f: 
        jsonStr = f.read()
        assert jsonLoads(jsonStr) == {"key": "value", "key-n": 101, "key-o": {"inner key": "inner value"}, "key-l": ["list value"]}

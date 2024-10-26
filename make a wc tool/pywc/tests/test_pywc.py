from pywc.pywc import get_counts
import os
import sys

def test_get_counts_on_txt(): 
    file_path = os.path.join(sys.path[0], 'tests', 'test.txt')
    print("file_path is", file_path)
    with open(file_path, 'rb') as f: 
        assert get_counts(f) == {'byte': 342190, 'char': 339292, 'line': 7145, 'word': 58164}
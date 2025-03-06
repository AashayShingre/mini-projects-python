from app.compress_tool import compressFile, decompressFile
import os
import sys


def compressionCheck(file_name):
    file_path = os.path.join(sys.path[0], "tests", file_name)
    compressed_file_path = os.path.join(sys.path[0], "tests", compressFile(file_path))
    decompressed_file_path = decompressFile(
        os.path.join(sys.path[0], "tests", compressed_file_path)
    )
    with open(file_path) as f1, open(decompressed_file_path) as f2:
        assert f1.read() == f2.read()
    print(compressed_file_path, decompressed_file_path, file_path)
    os.remove(compressed_file_path)
    os.remove(decompressed_file_path)


def test_testtxt():
    compressionCheck("test.txt")


def test_sometxt():
    compressionCheck("some.txt")


def test_atxt():
    compressionCheck("a.txt")

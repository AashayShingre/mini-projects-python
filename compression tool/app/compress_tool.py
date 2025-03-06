import argparse
from app.huffman import compressData, decompressData
import pickle
from bitarray import bitarray
import os
import re
import tempfile
import zipfile


def compress():
    """Entrypoint to the module. Reads file in text mode and writes the binary data onto other file. If the file already exists, returns ValueError"""
    parser = argparse.ArgumentParser(
        description="Lossless compress for text files. Uses huffman codes."
    )
    parser.add_argument("file", help="File name to encrypt/decrypt", nargs="*")
    parser.add_argument(
        "-d",
        "--decompress",
        action="store_true",
        required=False,
        help="decompresses the file",
    )
    parser.add_argument(
        "-c",
        "--compress",
        action="store_true",
        required=False,
        help="compresses the file",
    )

    args = parser.parse_args()

    if not (hasattr(args, "c") or hasattr(args, "d")):
        raise ValueError(
            "Only one flag `-c` or `-d` allowed. Check `--help` to know more."
        )

    if hasattr(args, "c") and hasattr(args, "d"):
        raise ValueError(
            "Either flag `-c` or `-d` required. Check '--help' to know more. "
        )

    if args.c:
        for fileName in args.file:
            compressFile(fileName)
    else:
        for fileName in args.file:
            decompressFile(fileName)


def compressFile(fileName) -> str:
    with open(fileName, newline="") as f:
        (huffmanTree, resultString, strLen) = compressData(f.read())

        # write huffmanTree and resultString into a separte tempfiles and zip them into result file
        with tempfile.NamedTemporaryFile() as metaFile, tempfile.NamedTemporaryFile() as dataFile:
            pickle.dump((huffmanTree, strLen), metaFile)
            metaFile.flush()  # tempfile.flush() moves it from buffer to disk

            if huffmanTree:
                bitarray(resultString).tofile(dataFile)
            else:
                dataFile.write(resultString.encode())
            dataFile.flush()

            resultFileName = f"{f.name}.compressed"
            counter = 1
            while os.path.exists(resultFileName):
                resultFileName = f"{f.name}.compressed{counter}"
                counter += 1

            with zipfile.ZipFile(resultFileName, "w") as zipf:
                zipf.write(metaFile.name, arcname="meta")
                zipf.write(dataFile.name, arcname="data")

            return resultFileName


def decompressFile(fileName) -> str:
    with zipfile.ZipFile(fileName, "r") as zipf:
        with zipf.open("meta", "r") as metaFile, zipf.open("data", "r") as dataFile:
            metaFile.seek(0)
            (tree, strLen) = pickle.load(metaFile)
            resultText: str
            if tree:
                compressedBitarray = bitarray()
                compressedBitarray.fromfile(dataFile)
                resultText = decompressData(strLen, tree=tree, bits=compressedBitarray)
            else:
                char = dataFile.read().decode()
                resultText = decompressData(strLen, char=char)

            orgFileName = re.sub(r"\.compressed\d*$", "", fileName)
            orgBaseName, extension = os.path.splitext(orgFileName)
            counter = 1
            while os.path.exists(f"{orgBaseName}{extension}"):
                orgBaseName = f"{orgBaseName}_{counter}"
                counter += 1

            resultFileName = f"{orgBaseName}{extension}"
            with open(resultFileName, "w") as resultf:
                resultf.write(resultText)

            return resultFileName

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
    parser = argparse.ArgumentParser(description="Lossless compress for text files. Uses huffman codes. Note that it'll be more size if the test size is not much.") 
    parser.add_argument("file", help="File name to encrypt/decrypt", nargs="*")
    parser.add_argument("-d", action="store_true", required=False, help="decompresses the file")
    parser.add_argument("-c", action="store_true", required=False, help="compresses the file") 

    args = parser.parse_args() 

    if (not (args.c or args.d)) or (args.c and args.d): 
        raise ValueError("Only one flag `-c` or `-d` mandatory. Check `-help` to know more.") 
    
    if args.c: 
        for fileName in args.file: 
            compressFile(fileName)                
    else: 
        for fileName in args.file: 
            decompressFile(fileName)



def compressFile(fileName): 
    with open(fileName) as f: 
        (huffmanTree, resultString, strLen) = compressData(f.read()) 

        with tempfile.NamedTemporaryFile() as metaFile, tempfile.NamedTemporaryFile() as dataFile:
            pickle.dump((huffmanTree, strLen), metaFile) 
            metaFile.flush()

            if huffmanTree: 
                bitarray(resultString).tofile(dataFile) # type: ignore
            else: 
                dataFile.write(resultString.encode())
            dataFile.flush()

            resultFileName = f"{f.name}.compressed"
            counter = 1
            while os.path.exists(resultFileName):
                resultFileName = f"{f.name}.{counter}.compressed"
                counter += 1

            zipPath = f"{resultFileName}"
            with zipfile.ZipFile(zipPath, 'w') as zipf:
                zipf.write(metaFile.name, arcname="meta")
                zipf.write(dataFile.name, arcname="data")


def decompressFile(fileName): 
    with zipfile.ZipFile(fileName, 'r') as zipf:
        with zipf.open("meta", 'r') as metaFile, zipf.open("data", 'r') as dataFile:
            metaFile.seek(0)
            (tree, strLen) = pickle.load(metaFile)
            resultText: str
            if tree:
                compressedBitarray = bitarray() 
                compressedBitarray.fromfile(dataFile) # type: ignore
                resultText = decompressData(strLen, tree=tree, bits=compressedBitarray)
            else: 
                char = dataFile.read().decode()
                resultText = decompressData(strLen, char=char)
            
            resultFileName = re.sub(r'\.compressed\d*$', '', fileName)
            counter = 1
            while os.path.exists(resultFileName+str(counter)): 
                counter += 1 
            
            with open(resultFileName+str(counter), 'w') as resultf: 
                resultf.write(resultText)







     
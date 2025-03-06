from __future__ import annotations
from typing import Optional, Iterable
from collections import Counter
from heapq import heapify, heappop, heappush
import functools


@functools.total_ordering  # sets __le___, __gt__, __ge__ etc from the mentioned two functions; will be used for heapify
class HuffmanNode:
    freq: int
    val: Optional[str]
    left: Optional[HuffmanNode]
    right: Optional[HuffmanNode]

    def __init__(self, freq, val=None, left=None, right=None):
        self.freq = freq
        self.val = val
        self.left = left
        self.right = right

    def __lt__(self, otherNode: HuffmanNode) -> bool:
        return self.freq < otherNode.freq

    def __eq__(self, otherNode: HuffmanNode) -> bool:
        return self.freq == otherNode.freq

    def __str__(self) -> str:  # TODO
        return f"{self.val} : [{self.left}, {self.right}]"


def buildTree(freqTable: dict[str, int]) -> HuffmanNode:
    """Creates huffman tree given the frequency of characters are dict"""
    if not freqTable:
        raise ValueError("buildTree: freqTable empty")

    minHeap = [HuffmanNode(freq, key) for key, freq in freqTable.items()]
    heapify(minHeap)

    while len(minHeap) > 1:
        leftNode = heappop(minHeap)
        rightNode = heappop(minHeap)
        parentNode = HuffmanNode(
            leftNode.freq + rightNode.freq, None, leftNode, rightNode
        )
        heappush(minHeap, parentNode)

    return minHeap[0]


def updateHuffmanTable(huffmanTable: dict[str, str], node: HuffmanNode, prefix: str):
    """Uses DFS to get the huffman code for each character"""
    if node.val:
        huffmanTable[node.val] = prefix
    else:
        if node.left and node.right:
            updateHuffmanTable(huffmanTable, node.left, prefix + "0")
            updateHuffmanTable(huffmanTable, node.right, prefix + "1")
        else:
            raise ValueError(
                f"updateHuffmanTable: Unknown error -> both left and right now expected {node}"
            )


def compressData(data: str) -> tuple[HuffmanNode | None, str, int]:
    """Takes the string data, builds tree, builds char map, returns result bitstring and the huffman tree"""
    if not data:
        raise ValueError("compressData: String empty")

    freqTable: dict[str, int] = Counter(data)
    if len(freqTable) >= 2:
        tree: HuffmanNode = buildTree(freqTable)
        huffmanTable: dict[str, str] = {}
        updateHuffmanTable(huffmanTable, tree, "")
        resultBitString = "".join(map(lambda char: huffmanTable[char], data))
        return (tree, resultBitString, len(data))
    else:
        resultString = data[0]
        return (None, resultString, len(data))


def decompressData(
    strLen: int,
    tree: Optional[HuffmanNode] = None,
    bits: Optional[Iterable] = None,
    char: Optional[str] = None,
) -> str:
    if bits and tree:
        resultChars = []
        ref = tree

        for bit in bits:
            if not ref:
                raise ValueError(
                    f"decompressData: Unexpected set of bits for tree {tree}"
                )
            ref = ref.right if bit else ref.left
            if ref and ref.val:  # encountered leaf
                resultChars.append(ref.val)
                if len(resultChars) == strLen:
                    break
                ref = tree  # moving back to the top

        return "".join(resultChars)

    if char:
        return char * strLen

    raise ValueError("decompressData: Unknown parameters")

from __future__ import annotations

from typing import Optional

from ordered_list import (OrderedList, insert, pop, size)


class HuffmanNode:
    """Represents a node in a Huffman tree.

    Attributes:
        char: The character as an integer ASCII value
        frequency: The frequency of the character in the file
        left: The left Huffman sub-tree
        right: The right Huffman sub-tree
    """
    def __init__(
            self,
            char: int,
            frequency: int,
            left: Optional[HuffmanNode] = None,
            right: Optional[HuffmanNode] = None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

    def __eq__(self, other) -> bool:
        """Returns True if and only if self and other are equal."""
        return (
            isinstance(other, HuffmanNode) and
            other.char == self.char and
            other.frequency == self.frequency and
            other.left == self.left and
            other.right == self.right
        )

    def __lt__(self, other) -> bool:
        """Returns True if and only if self < other."""
        if self.frequency == other.frequency:
            return self.char < other.char
        else:
            return self.frequency < other.frequency


def count_frequencies(filename: str) -> list[int]:
    """Reads the given file and counts the frequency of each character.

    The resulting Python list will be of length 256, where the indices
    are the ASCII values of the characters, and the value at a given
    index is the frequency with which that character occured.
    """
    lst = [0] * 256
    with open(filename) as file:
        for line in file:
            for char in line:
                index = ord(char)
                lst[index] += 1

    return lst


def build_huffman_tree(frequencies: list[int]) -> Optional[HuffmanNode]:
    """Creates a Huffman tree of the characters with non-zero frequency.

    Returns the root of the tree.
    """
    if (empty_lst(frequencies)):
        return None
    elif check_freq(frequencies) == 1:
        for x in range(len(frequencies)):
            if frequencies[x] > 0:
                return HuffmanNode(x, frequencies[x])
    else:
        lst = OrderedList()
        for x in range(len(frequencies)):
            if frequencies[x] > 0:
                new_node = HuffmanNode(x, frequencies[x])
                insert(lst, new_node)
        while size(lst) > 1:
            left = pop(lst, 0)
            right = pop(lst, 0)
            if left.char < right.char:
                new_node = HuffmanNode(
                    left.char,
                    left.frequency + right.frequency,
                    left, right
                )
            else:
                new_node = HuffmanNode(
                    right.char,
                    left.frequency + right.frequency,
                    left, right
                )
            insert(lst, new_node)
        tree = pop(lst, 0)
    return tree


def create_codes(tree: Optional[HuffmanNode]) -> list[str]:
    """Traverses the tree creating the Huffman code for each character.

    The resulting Python list will be of length 256, where the indices
    are the ASCII values of the characters, and the value at a given
    index is the Huffman code for that character.
    """
    code = [''] * 256
    code = tree_code(tree, code, "")
    return code


def create_header(frequencies: list[int]) -> str:
    """Returns the header for the compressed Huffman data.

    For example, given the file "aaaccbbbb", this would return:
    "97 3 98 4 99 2"
    """
    header = ''
    for i in range(256):
        if frequencies[i] > 0:
            header += str(i) + ' ' + str(frequencies[i]) + ' '
    header = header.rstrip()
    return header


def huffman_encode(in_filename: str, out_filename: str) -> None:
    """Encodes the data in the input file, writing the result to the
    output file."""
    tree = None
    freq = count_frequencies(in_filename)
    tree = build_huffman_tree(freq)
    code_lst = create_codes(tree)
    header = create_header(freq)
    encode = ''
    with open(in_filename) as in_file:
        for line in in_file:
            for char in line:
                encode += code_lst[ord(char)]

    with open(out_filename, 'w') as out_file:
        out_file.write(header)
        out_file.write('\n')
        out_file.write(encode)


def huffman_decode(in_filename: str, out_filename: str) -> None:
    decode = ''
    tree = None
    lst = []
    with open(in_filename) as in_file:
        lst = parse_header(in_file.readline())
        if empty_lst(lst):
            decode = ''
        elif check_freq(lst) == 1:
            for i in range(len(lst)):
                if lst[i] != 0:
                    for x in range(lst[i]):
                        decode += chr(i)
        else:
            tree = build_huffman_tree(lst)
            temp = tree
            for line in in_file:
                for char in line:
                    if char == '0':
                        temp = temp.left
                    elif char == '1':
                        temp = temp.right
                    if temp.left is None and temp.right is None:
                        decode += chr(temp.char)
                        temp = tree

    with open(out_filename, 'w') as out_file:
        out_file.write(decode)


def parse_header(header: str) -> list:
    lst = [0] * 256
    if header == '\n':
        return lst
    header = header.split(' ')
    i = 0
    while True:
        lst[int(header[i])] = int(header[i + 1])
        if i + 2 >= len(header):
            break
        else:
            i += 2
    return lst


def tree_code(tree, code, value):
    if tree:
        if tree.left is None and tree.right is None:
            code[tree.char] += value
        tree_code(tree.left, code, value + '0')
        tree_code(tree.right, code, value + '1')
    return code


def empty_lst(frequencies):
    for i in frequencies:
        if i > 0:
            return False
    return True


def check_freq(frequencies):
    x = 0
    for i in frequencies:
        if i > 0:
            x += 1
    return x

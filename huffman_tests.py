import unittest
import subprocess

# NOTE: Do not import anything else from huffman.  If you do, your tests
# will crash when I test them.  You shouldn't need to test your helper
# functions directly, just via testing the required functions.
from huffman import (
    HuffmanNode, count_frequencies, build_huffman_tree, create_codes,
    create_header, huffman_encode, parse_header, huffman_decode)


class TestList(unittest.TestCase):
    def test_count_frequencies_01(self):
        frequencies = count_frequencies("text_files/file2.txt")
        expected = [0, 2, 4, 8, 16, 0, 2, 0]

        self.assertEqual(frequencies[96:104], expected)

    def test_node_lt_01(self):
        node1 = HuffmanNode(97, 10)
        node2 = HuffmanNode(65, 20)

        self.assertLess(node1, node2)
        self.assertGreater(node2, node1)

    def test_build_huffman_tree_01(self):
        frequencies = [0] * 256
        frequencies[97] = 5
        frequencies[98] = 10

        huffman_tree = build_huffman_tree(frequencies)

        # NOTE: This also requires a working __eq__ for your HuffmanNode
        self.assertEqual(
            huffman_tree,
            HuffmanNode(97, 15, HuffmanNode(97, 5), HuffmanNode(98, 10))
        )

    def test_build_huffman_tree_02(self):
        frequecies = [0] * 256
        tree = build_huffman_tree(frequecies)
        self.assertIsNone(tree)

    def test_build_huffman_tree_03(self):
        freequencies = [0] * 256
        freequencies[90] = 6
        tree = build_huffman_tree(freequencies)
        node1 = HuffmanNode(90, 6)
        self.assertEqual(tree, node1)

    def test_create_codes_01(self):
        huffman_tree = HuffmanNode(
            97, 15,
            HuffmanNode(97, 5),
            HuffmanNode(98, 10)
        )

        codes = create_codes(huffman_tree)
        self.assertEqual(codes[ord('a')], '0')
        self.assertEqual(codes[ord('b')], '1')

    def test_create_codes_02(self):
        freq = [0] * 256
        tree = build_huffman_tree(freq)
        code = create_codes(tree)
        lst = [''] * 256
        self.assertEqual(code, lst)

    def test_create_code_03(self):
        freq = [0] * 256
        freq[2] = 1
        tree = build_huffman_tree(freq)
        code = create_codes(tree)
        lst = [''] * 256
        self.assertEqual(code, lst)

    def test_create_header_01(self):
        frequencies = [0] * 256
        frequencies[97] = 5
        frequencies[98] = 10

        self.assertEqual(create_header(frequencies), "97 5 98 10")

    def test_huffman_encode_01(self):
        huffman_encode("text_files/file1.txt", "text_files/file1_out.txt")

        result = subprocess.run(
            ['diff',
             '--strip-trailing-cr',
             'text_files/file1_out.txt',
             'text_files/file1_soln.txt'],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_huffman_encode2(self):
        huffman_encode(
            'text_files/multiline.txt',
            'text_files/multiline_out.txt')
        result = subprocess.run(
            ['diff',
             '--strip-trailing-cr',
             'text_files/multiline_out.txt',
             'text_files/multiline_soln.txt'],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_huffman_encode3(self):
        huffman_encode(
            'text_files/1char.txt',
            'text_files/1char_out.txt'
        )
        result = subprocess.run(
            ['diff',
             '--strip-trailing-cr',
             'text_files/1char_out.txt',
             'text_files/1char_soln.txt'],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_huffman_encode4(self):
        huffman_encode(
            'text_files/empty_file.txt',
            'text_files/empty_out.txt'
        )
        result = subprocess.run(
            ['diff',
             '--strip-trailing-cr',
             'text_files/empty_out.txt',
             'text_files/empty_soln.txt'],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_huffman_encode(self):
        huffman_encode(
            'text_files/declaration.txt',
            'text_files/declaration_out.txt'
        )
        result = subprocess.run(
            ['diff',
             '--strip-trailing-cr',
             'text_files/declaration_out.txt',
             'text_files/declaration_soln.txt'],
            check=False,
            text=True,
            capture_output=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_parse_header(self):
        str1 = '\n'
        str2 = '97 3'
        lst = [0] * 256
        lst2 = [0] * 256
        lst[97] = 3
        self.assertEqual(parse_header(str1), lst2)
        self.assertEqual(parse_header(str2), lst)

    def test_decode1(self):
        huffman_decode(
            'text_files/declaration_soln.txt',
            'text_files/declaration_decoded.txt'
        )
        with open("text_files/declaration_decoded.txt") as student_out, \
                open("text_files/declaration.txt") as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())

    def test_decode2(self):
        huffman_decode(
            'text_files/empty_soln.txt',
            'text_files/empty_decoded.txt'
        )
        with open("text_files/empty_decoded.txt") as student_out, \
                open("text_files/empty_file.txt") as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())

    def test_decode3(self):
        huffman_decode(
            'text_files/1char_soln.txt',
            'text_files/1char_decoded.txt'
        )
        with open("text_files/1char_decoded.txt") as student_out, \
                open("text_files/1char.txt") as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())

    def test_parse_header_01(self):
        header = "97 2 98 4 99 8 100 16 102 2\n"
        frequencies = parse_header(header)
        expected = [0, 2, 4, 8, 16, 0, 2, 0]
        self.assertEqual(frequencies[96:104], expected)

    def test_huffman_decode_01(self):
        huffman_decode(
            "text_files/file1_soln.txt",
            "text_files/file1_decoded.txt"
        )
        with open("text_files/file1_decoded.txt") as student_out, \
                open("text_files/file1.txt") as correct_out:
            self.assertEqual(student_out.read(), correct_out.read())


if __name__ == '__main__':
    unittest.main()

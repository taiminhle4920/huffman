import unittest
from huffman import HuffmanNode, tree_code, empty_lst, check_freq


class TestList(unittest.TestCase):
    def test_tree_code(self):
        tree = HuffmanNode(97, 4)
        tree.left = HuffmanNode(97, 2)
        tree.right = HuffmanNode(99, 2)
        lst = [''] * 256
        lst = tree_code(tree, lst, '')
        lst2 = [''] * 256
        lst2[97] = '0'
        lst2[99] = '1'
        self.assertEqual(lst, lst2)

    def test_empty_lst(self):
        lst = [0] * 256
        self.assertTrue(empty_lst(lst))
        lst[1] = 2
        self.assertFalse(empty_lst(lst))

    def test_check_freq(self):
        lst = [0] * 256
        lst[1] = 2
        lst[2] = 3
        self.assertEqual(check_freq(lst), 2)


if __name__ == '__main__':
    unittest.main()

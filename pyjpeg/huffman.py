import queue


class HuffmanNode(object):
    def __init__(self, left=None, right=None, root=None):
        self.left = left
        self.right = right
        self.root = root #?

    def children(self):
        return (self.left, self.right)


def create_huffman_table(BITS, HUFFVAL):
    kk, j = 0, 1

    HUFFSIZE = [] * len()
    for ii in range(16):
        if j > BITS[ii]:
            j = 1
        else:
            HUFFSIZE[kk] = ii
            k += 1
            j += 1
            continue

    HUFFSIZE[k] = 0
    lastk = k

    return HUFFSIZE

'''
Number of codes of a given length, 1 to 16
elements of the list BITS
0, 2, 2, 3, 1, 1, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0

Value associated with each huffman code
For each code length, ii, the value associated with each huffman code of length ii.
elements of the list HUFFVAL
1: None,
2: 0, 1 : 0b00, 0b01
3: 2, 5 : 0b010, 0b101
4: 3, 4, 6,
5: 7
6: 8
7: None
8: None
9: None
...

+--------+-----------+------+
| Length | Bits      | Code |
+========+===========+======+
| 1      |           |      |
+--------+-----------+------+
| 2      | 00        | 00   |
|        | 01        | 01   |
+--------+-----------+------+
| 3      | 100       | 02   |
|        | 101       | 05   |
+--------+-----------+------+
| 4      | 1100      | 03   |
|        | 1101      | 04   |
|        | 1110      | 06   |
+--------+-----------+------+
| 5      | 1111 0    | 07   |
+--------+-----------+------+
| 6      | 1111 10   | 08   |
+--------+-----------+------+
| 7      |           |      |
+--------+-----------+------+
| 8      |           |      |
+--------+-----------+------+
| 9      |           |      |
+--------+-----------+------+
| 10     |           |      |
+--------+-----------+------+
| 11     |           |      |
+--------+-----------+------+
| 12     |           |      |
+--------+-----------+------+
| 13     |           |      |
+--------+-----------+------+
| 14     |           |      |
+--------+-----------+------+
| 15     |           |      |
+--------+-----------+------+
| 16     |           |      |
+--------+-----------+------+

'''

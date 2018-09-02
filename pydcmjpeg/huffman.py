"""Functions for creating Huffman tables."""

import heapq


def get_huffman_table(bits, huffval, method='default'):
    """Return the Huffman table for `bits`, `huffval`

    Parameters
    ----------
    bits : list of int
        The number of Huffman codes for each of the 16 possible lengths allowed
        by 10918. Corresponds to the Huffman BITS list.
    huffval : dict of list of int
        The values associated with each Huffman code length. The keys to the
        dict are the Huffman codes lengths.

    Returns
    -------
    Uh...?

    References
    ----------
    ISO/IEC 10918-1
    """
    if method == 'default':
        return _get_huffman_heapq(bits, huffval)
    else:
        raise ValueError(
            "Unknown method '{}' for building a Huffman table".format(method)
        )


def _get_huffman_heapq(bits, huffval):
    """Use python's heapq to build a Huffman tree."""
    pass



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

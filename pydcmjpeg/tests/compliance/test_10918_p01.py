"""Tests for pydcmjpeg.fileio module."""

import os

import numpy as np
import pytest

from pydcmjpeg.fileio import jpgread


COMPL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../', 'data', 'compliance')
)
C10918_PROCESS01 = os.path.join(COMPL_DIR, '10918', 'process_01')
C10918_PROCESS02 = os.path.join(COMPL_DIR, '10918', 'process_02')
C10918_PROCESS04 = os.path.join(COMPL_DIR, '10918', 'process_04')
C10918_PROCESS14 = os.path.join(COMPL_DIR, '10918', 'process_14')

# Process 1 compliance files
PROCESS01_A1 = os.path.join(C10918_PROCESS01, 'A1.JPG')
PROCESS01_B1 = os.path.join(C10918_PROCESS01, 'B1.JPG')
PROCESS01_B2 = os.path.join(C10918_PROCESS01, 'B2.JPG')
PROCESS01_DREF_A8  = os.path.join(C10918_PROCESS01, 'DREF_A8.DCT')
PROCESS01_DREF_B8  = os.path.join(C10918_PROCESS01, 'DREF_B8.DCT')
PROCESS01_DREF_C8  = os.path.join(C10918_PROCESS01, 'DREF_C8.DCT')
PROCESS01_DREF_D8  = os.path.join(C10918_PROCESS01, 'DREF_D8.DCT')


QUANTIZATION_A = np.asarray(
    [[ 8,  6,  5,  8, 12, 20, 26, 30],
     [ 6,  6,  7, 10, 13, 29, 30, 28],
     [ 7,  7,  8, 12, 20, 29, 35, 28],
     [ 7,  9, 11, 15, 26, 44, 40, 31],
     [ 9, 11, 19, 28, 34, 55, 52, 39],
     [12, 18, 28, 32, 41, 52, 57, 46],
     [25, 32, 39, 44, 52, 61, 60, 51],
     [36, 46, 48, 49, 56, 50, 52, 50]]
)

QUANTIZATION_B = np.asarray(
    [[ 9,  9, 12, 24, 50, 50, 50, 50],
     [ 9, 11, 13, 33, 50, 50, 50, 50],
     [12, 13, 28, 50, 50, 50, 50, 50],
     [24, 33, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50]]
)

QUANTIZATION_C = np.asarray(
    [[16, 17, 18, 19, 20, 21, 22, 23],
     [17, 18, 19, 20, 21, 22, 23, 24],
     [18 ,19, 20, 21, 22, 23, 24, 25],
     [19, 20, 21, 22, 23, 24, 25, 26],
     [20, 21, 22, 23, 24, 25, 26, 27],
     [21, 22, 23, 24, 25, 26, 27, 28],
     [22, 23, 24, 25, 26, 27, 28, 29],
     [23, 24, 25, 26, 27, 28, 29, 30]]
)

QUANTIZATION_D = np.asarray(
    [[16, 16, 19, 22, 26, 27, 29, 34],
     [16, 16, 22, 24, 27, 29, 34, 37],
     [19, 22, 26, 27, 29, 34, 34, 38],
     [22, 22, 26, 27, 29, 34, 37, 40],
     [22, 26, 27, 29, 32, 35, 40, 48],
     [26, 27, 29, 32, 25, 40, 48, 58],
     [26, 27, 29, 34, 38, 46, 56, 69],
     [27, 29, 35, 38, 46, 56, 69, 83]]
)


class TestJPEGProcess01_Decode(object):
    """JPEG 10918-2 compliance tests for decoding Process 1.

    8-bit baseline sequential DCT.

    Tests
    -----
    Test A
        Compressed image test data stream A1:
        * Interchange format syntax
        * 4 components
        * A single interleaved scan
        * Restart interval = 1/2 block row - 1

    Test B
        Compressed image test data stream B1:
        * Abbreviated format syntax
        * Huffman and quantization table
        * No entropy coded segments

        Compressed image test data stream B2:
        * Abbreviated format syntax
        * 255 components non-interleaved

    """
    def setup(self):
        # JPEGs
        self.JPG_A1 = PROCESS01_A1
        self.JPG_B1 = PROCESS01_B1
        self.JPG_B2 = PROCESS01_B2

        # DCTs
        self.DCT_A8 = PROCESS01_DREF_A8
        self.DCT_B8 = PROCESS01_DREF_B8
        self.DCT_C8 = PROCESS01_DREF_C8
        self.DCT_D8 = PROCESS01_DREF_D8

    def test_find_soi(self):
        pass

    def test_check_frame(self):
        pass

    def test_eoi(self):
        pass

    def test_all_required_markers_found(self):
        """Required markers are:

        SOI, EOI, SOS, SOF_0, DQT, DHT
        """
        pass

    def test_marker_order_ok(self):
        pass

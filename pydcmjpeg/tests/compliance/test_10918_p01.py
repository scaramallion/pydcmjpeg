"""Tests for pydcmjpeg.fileio module."""

import filecmp
import os
from tempfile import NamedTemporaryFile
from struct import unpack

import numpy as np
import pytest

from pydcmjpeg._markers import MARKERS
from pydcmjpeg.config import ZIGZAG
from pydcmjpeg.fileio import jpgread, parse_jpg


COMPL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../', '../', 'data', 'compliance')
)
C10918_PROCESS01 = os.path.join(COMPL_DIR, '10918', 'process_01')
#C10918_PROCESS02 = os.path.join(COMPL_DIR, '10918', 'process_02')
#C10918_PROCESS04 = os.path.join(COMPL_DIR, '10918', 'process_04')
#C10918_PROCESS14 = os.path.join(COMPL_DIR, '10918', 'process_14')

# Process 1 compliance files
PROCESS01_A1 = os.path.join(C10918_PROCESS01, 'A1.JPG')
PROCESS01_B1 = os.path.join(C10918_PROCESS01, 'B1.JPG')
PROCESS01_B2 = os.path.join(C10918_PROCESS01, 'B2.JPG')
PROCESS01_A1_REF = os.path.join(C10918_PROCESS01, 'A1.TXT')
PROCESS01_B1_REF = os.path.join(C10918_PROCESS01, 'B1.TXT')
PROCESS01_B2_REF = os.path.join(C10918_PROCESS01, 'B2.TXT')
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


def _write_soi(fp, offset, marker, name, info):
    fp.write('{0:<7}{1:<4}({2})\n'.format(offset, name, marker))

def _write_com(fp, offset, marker, name, info):
    comment = "'" + info['Cm'] + "'"
    # First line has 46 characters, the remaining is 63 characters/line
    fp.write(
        "{0:<7}{1:<4}({2}) Lc={3} {4}\n"
        .format(offset, name, marker, info['Lc'], comment[:47])
    )
    comment = comment[47:]

    while True:
        if not comment:
            break
        line = comment[:63]
        comment = comment[63:]

        fp.write("         {}\n".format(line))

def _write_dqt(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lq={3}\n"
        .format(offset, name, marker, info['Lq'])
    )
    for pq, tq, qk in zip(info['Pq'], info['Tq'], info['Qk']):
        _prec = '2' if pq else '1'
        fp.write(
            'Qtable {0},  Precision = {1} byte.\n'.format(tq, _prec)
        )
        #for ii in range(0, 64, 8):
        #    print('      ', '   '.join(['{:>2}'.format(ii) for ii in Q_k[ii:ii+8]]))
        new_qk = []
        for index in ZIGZAG:
            new_qk.append(qk[index])

        for ii in range(0, 64, 8):
            _line = '   '.join(['{:>2}'.format(qq) for qq in new_qk[ii:ii + 8]])
            fp.write('             {}\n'.format(_line))

def _write_dri(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lr={3} Ri={4}\n"
        .format(offset, name, marker, info['Lr'], info['Ri'])
    )

def _write_sof(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lf={3} P={4} Y={5} X={6} Nf={7}"
        .format(offset, name, marker, info['Lf'], info['P'], info['Y'],
        info['X'], info['Nf'])
    )
    if name == 'SOF0':
        fp.write('  (baseline seq. DCT)\n')
    else:
        raise NotImplementedError

    for ci, h, v, tqi in zip(info['Ci'], info['Hi'], info['Vi'], info['Tqi']):
        fp.write(
            '             Ci={0:>3} HV={1}{2} Tqi={3}\n'
            .format(ci, h, v, tqi)
        )

def _write_dht(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lq={3}\n"
        .format(offset, name, marker, info['Lh'])
    )
    for tc, th, li, vij in zip(info['Tc'], info['Th'], info['Li'], info['Vij']):
        if tc == 0:
            fp.write('Lossless/DC Huffman table {}\n'.format(th))
        elif tc == 1:
            fp.write('AC Huffman table {}\n'.format(th))
        else:
            raise NotImplementedError

        fp.write(':(  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16   code lengths       )\n')
        nr_values = ' '.join(['{:>02x}'.format(val) for val in li])
        fp.write('   {} :(values/length (hex))\n'.format(nr_values))

        for ii, values in enumerate(vij):
            if values is not None:
                for jj in range(0, len(values), 16):
                    val = ' '.join(['{:>02x}'.format(vv) for vv in values[jj:jj+16]])
                    fp.write('   {:<47}'.format(val))
                    fp.write(' :(hex values, L={:>2})\n'.format(ii + 1))

def _write_app(fp, offset, marker, name, info):
    app = info['Ap'].decode('utf-8')
    app_info = "'" + app + "'"
    # First line has 46 characters, the remaining is 63 characters/line
    fp.write(
        "{0:<7}{1:<4}({2}) Lp={3} {4}\n"
        .format(offset, name, marker, info['Lp'], app_info[:47])
    )

    for ii in range(46, len(app_info), 63):
        fp.write("         {}\n".format(app_info[ii:ii + 63]))

def _write_sos(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Ls={3} Ns={4}\n"
        .format(offset, name, marker, info['Ls'], info['Ns'])
    )

    for csk, td, ta in zip(info['Csj'], info['Tdj'], info['Taj']):
        fp.write(
            '             Csk={0:>3} Td={1} Ta={2}\n'
            .format(csk, td, ta)
        )

    fp.write(
        '             Ss={} Se={} Ah={} Al={}\n'
        .format(info['Ss'], info['Se'], info['Ah'], info['Al'])
    )

def _write_eoi(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2})\n"
        .format(offset, name, marker)
    )

WRITERS = {
    'SOI' : _write_soi,
    'COM' : _write_com,
    'DQT' : _write_dqt,
    'DRI' : _write_dri,
    'SOF' : _write_sof,
    'DHT' : _write_dht,
    'APP' : _write_app,
    'SOS' : _write_sos,
    'EOI' : _write_eoi,
}


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

    def test_parse_a1(self):
        """Test that parsing the A1 file produces the correct output."""
        with open(PROCESS01_A1, 'rb') as fp:
            info = parse_jpg(fp)
            file_length = fp.tell()

        # Order by offset
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))

        tempfile = NamedTemporaryFile()
        with open(tempfile.name, 'w') as tfile:
            tfile.write(
                "Parsed version of ' testa1 hdr p', May 8, 1994, "
                "WBP and JLM (IBM)\n"
            )
            # Data
            for key in keys:
                writer = WRITERS[key[:3]]
                (marker, fill_bytes, data) = info[key]
                marker = '{:04x}'.format(marker)
                (name, offset) = key.split('@')
                if fill_bytes:
                    marker = 'ff' * fill_bytes + marker
                    tfile.write('      {:>2} FIL bytes\n'.format(fill_bytes))
                writer(tfile, offset, marker, name, data)

            # End
            tfile.write(
                '{} markers found in {} bytes of compressed data\n'
                .format(len(keys), file_length)
            )
            tfile.seek(0)

        with open(tempfile.name, 'r') as tfile:
            with open(PROCESS01_A1_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

    def test_parse_b1(self):
        """Test that parsing the B1 file produces the correct output."""
        with open(PROCESS01_B1, 'rb') as fp:
            info = parse_jpg(fp)
            file_length = fp.tell()

        # Order by offset
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))

        tempfile = NamedTemporaryFile()
        with open(tempfile.name, 'w') as tfile:
            tfile.write(
                "Parser output for ' testb1.jpg', May 8, 1994, "
                "WBP and JLM (IBM)\n"
            )
            # Data
            for key in keys:
                writer = WRITERS[key[:3]]
                (marker, fill_bytes, data) = info[key]
                marker = '{:04x}'.format(marker)
                (name, offset) = key.split('@')
                if fill_bytes:
                    marker = 'ff' * fill_bytes + marker
                    tfile.write('      {:>2} FIL bytes\n'.format(fill_bytes))
                writer(tfile, offset, marker, name, data)

            # End
            tfile.write(
                '{} markers found in {} bytes of compressed data\n'
                .format(len(keys), file_length)
            )
            tfile.seek(0)

        with open(tempfile.name, 'r') as tfile:
            with open(PROCESS01_B1_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

    def test_parse_b2(self):
        """Test that parsing the B2 file produces the correct output."""
        with open(PROCESS01_B2, 'rb') as fp:
            info = parse_jpg(fp)
            file_length = fp.tell()

        # Order by offset
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))

        tempfile = NamedTemporaryFile()
        with open(tempfile.name, 'w') as tfile:
            tfile.write(
                "Parsed version of ' testb2 hdr p', May 8, 1994, "
                "WBP and JLM (IBM)\n"
            )
            # Data
            for key in keys:
                writer = WRITERS[key[:3]]
                (marker, fill_bytes, data) = info[key]
                marker = '{:04x}'.format(marker)
                (name, offset) = key.split('@')
                if fill_bytes:
                    marker = 'ff' * fill_bytes + marker
                    tfile.write('      {:>2} FIL bytes\n'.format(fill_bytes))
                writer(tfile, offset, marker, name, data)

            # End
            tfile.write(
                '{} markers found in {} bytes of compressed data\n'
                .format(len(keys), file_length)
            )
            tfile.seek(0)

        with open(tempfile.name, 'r') as tfile:
            with open(PROCESS01_B2_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

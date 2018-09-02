"""Compliance tests for 10918 Process 2."""

import os
from tempfile import NamedTemporaryFile

import pytest

from pydcmjpeg._markers import MARKERS
from pydcmjpeg.fileio import jpgread, parse_jpg

from pydcmjpeg.tests.compliance import _common as COMMON
from ._common import WRITERS


COMPL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../', '../', 'data', 'compliance')
)

C10918_PROCESS02 = os.path.join(COMPL_DIR, '10918', 'process_02')

# Process 1 compliance files
PROCESS02_A1 = os.path.join(C10918_PROCESS02, 'A1.JPG')
PROCESS02_B1 = os.path.join(C10918_PROCESS02, 'B1.JPG')
PROCESS02_B2 = os.path.join(C10918_PROCESS02, 'B2.JPG')
PROCESS02_C1 = os.path.join(C10918_PROCESS02, 'C1.JPG')
PROCESS02_C2 = os.path.join(C10918_PROCESS02, 'C2.JPG')
PROCESS02_A1_REF = os.path.join(C10918_PROCESS02, 'A1.TXT')
PROCESS02_B1_REF = os.path.join(C10918_PROCESS02, 'B1.TXT')
PROCESS02_B2_REF = os.path.join(C10918_PROCESS02, 'B2.TXT')
PROCESS02_C1_REF = os.path.join(C10918_PROCESS02, 'C1.TXT')
PROCESS02_C2_REF = os.path.join(C10918_PROCESS02, 'C2.TXT')
PROCESS02_DREF_A8  = os.path.join(C10918_PROCESS02, 'DREF_A8.DCT')
PROCESS02_DREF_B8  = os.path.join(C10918_PROCESS02, 'DREF_B8.DCT')
PROCESS02_DREF_C8  = os.path.join(C10918_PROCESS02, 'DREF_C8.DCT')
PROCESS02_DREF_D8  = os.path.join(C10918_PROCESS02, 'DREF_D8.DCT')


class TestJPEGProcess02_Parse(object):
    """JPEG 10918-2 compliance tests for parsing Process 2.

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

    Test C
        C1:
        * Interleaved

        C2:
        * Non-interleaved

    """
    def test_find_soi(self):
        pass

    def test_check_frame(self):
        pass

    def test_eoi(self):
        pass

    def test_all_required_markers_found(self):
        """Required markers are:

        SOI, EOI, SOS, SOF0, DQT, DHT
        """
        # A1  and B2 are interchange format
        required_keys = ['SOI', 'EOI', 'SOS', 'SOF0', 'DQT', 'DHT']
        optional_keys = ['RST0', 'RST1', 'RST2', 'RST3', 'RST4', 'RST5',
                         'RST6', 'RST7', 'DNL', 'DAC', 'DRI', 'COM', 'APP0',
                         'APP1', 'APP2', 'APP3', 'APP4', 'APP5', 'APP6',
                         'APP7', 'APP8', 'APP9', 'APP10', 'APP11', 'APP12',
                         'APP13', 'APP14', 'APP15']
        for info in [parse_jpg(open(PROCESS02_A1, 'rb')),  parse_jpg(open(PROCESS02_B2, 'rb'))]:
            keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))
            keys = [kk.split('@')[0] for kk in keys]
            # Markers with (G) must be present
            for marker in required_keys:
                assert marker in keys

            # Markers with (-) or missing markers should not be present
            for marker in keys:
                assert marker in required_keys + optional_keys

        # B1 is in the abbreviated format
        required_keys = ['SOI', 'EOI']
        optional_keys = ['DQT', 'DHT', 'COM', 'APP0',
                         'APP1', 'APP2', 'APP3', 'APP4', 'APP5', 'APP6',
                         'APP7', 'APP8', 'APP9', 'APP10', 'APP11', 'APP12',
                         'APP13', 'APP14', 'APP15']


        info = parse_jpg(open(PROCESS02_B1, 'rb'))
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))
        keys = [kk.split('@')[0] for kk in keys]
        # Markers with (G) must be present
        for marker in required_keys:
            assert marker in keys

        # Markers with (-) or missing markers should not be present
        for marker in keys:
            assert marker in required_keys + optional_keys

    def test_marker_order_ok(self):
        pass

    def test_parse_a1(self):
        """Test that parsing the A1 file produces the correct output."""
        with open(PROCESS02_A1, 'rb') as fp:
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
            with open(PROCESS02_A1_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

    def test_parse_b1(self):
        """Test that parsing the B1 file produces the correct output."""
        with open(PROCESS02_B1, 'rb') as fp:
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
            with open(PROCESS02_B1_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

    def test_parse_b2(self):
        """Test that parsing the B2 file produces the correct output."""
        with open(PROCESS02_B2, 'rb') as fp:
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
            with open(PROCESS02_B2_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

    def test_parse_c1(self):
        """Test that parsing the C1 file produces the correct output."""
        COMMON.WRITE_SOS_DATA = True

        with open(PROCESS02_C1, 'rb') as fp:
            info = parse_jpg(fp)
            file_length = fp.tell()

        # Order by offset
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))

        tempfile = NamedTemporaryFile()
        with open(tempfile.name, 'w') as tfile:
            tfile.write(
                "Parser output for 'testc1.jpg', May 8, 1994, "
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
            sos_markers = 0
            sos_keys = [kk for kk in keys if 'SOS' in kk]
            for key in sos_keys:
                # SOS contains (N - 9) markers
                _markers = [mm for mm in info[key][2].keys() if 'RST' in mm]
                sos_markers += len(_markers)

            total_markers = len(keys) + sos_markers
            tfile.write(
                '{} markers found in {} bytes of compressed data\n'
                .format(total_markers, file_length)
            )
            tfile.seek(0)

            COMMON.WRITE_SOS_DATA = False

        with open(tempfile.name, 'r') as tfile:
            with open(PROCESS02_C1_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

    def test_parse_c2(self):
        """Test that parsing the C2 file produces the correct output."""
        COMMON.WRITE_SOS_DATA = True

        with open(PROCESS02_C2, 'rb') as fp:
            info = parse_jpg(fp)
            file_length = fp.tell()

        # Order by offset
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))

        tempfile = NamedTemporaryFile()
        with open(tempfile.name, 'w') as tfile:
            tfile.write(
                "Parser output for 'testc2.jpg', May 8, 1994, "
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
            sos_markers = 0
            sos_keys = [kk for kk in keys if 'SOS' in kk]
            for key in sos_keys:
                # SOS contains (N - 9) markers
                _markers = [mm for mm in info[key][2].keys() if 'RST' in mm]
                sos_markers += len(_markers)

            total_markers = len(keys) + sos_markers
            tfile.write(
                '{} markers found in {} bytes of compressed data\n'
                .format(total_markers, file_length)
            )
            tfile.seek(0)

            COMMON.WRITE_SOS_DATA = False

        with open(tempfile.name, 'r') as tfile:
            with open(PROCESS02_C2_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

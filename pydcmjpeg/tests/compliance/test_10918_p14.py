"""Compliance tests for 10918 Process 4."""

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

C10918_PROCESS14 = os.path.join(COMPL_DIR, '10918', 'process_14')

# Process 1 compliance files
PROCESS14_O1 = os.path.join(C10918_PROCESS14, 'O1.JPG')
PROCESS14_O2 = os.path.join(C10918_PROCESS14, 'O2.JPG')
PROCESS14_O1_REF = os.path.join(C10918_PROCESS14, 'O1.TXT')
PROCESS14_O2_REF = os.path.join(C10918_PROCESS14, 'O2.TXT')


class TestJPEGProcess14_Parse(object):
    """JPEG 10918-2 compliance tests for parsing Process 14.

    Tests
    -----
    Test O:
        O1:
        * 8-bit
        * Interleaved

        O2:
        * 16-bit
        * Non-interleaved
    """
    def test_find_soi(self):
        pass

    def test_check_frame(self):
        pass

    def test_eoi(self):
        pass

    def test_marker_order_ok(self):
        pass

    def test_parse_o1(self):
        """Test that parsing the O1 file produces the correct output."""
        COMMON.WRITE_SOS_DATA = True
        COMMON.WRITE_SOS_TYPE = 'Lossless'

        with open(PROCESS14_O1, 'rb') as fp:
            info = parse_jpg(fp)
            file_length = fp.tell()

        # Order by offset
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))

        tempfile = NamedTemporaryFile()
        with open(tempfile.name, 'w') as tfile:
            tfile.write(
                "Parser output for 'testo1.jpg', May 11, 1994, "
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
            COMMON.WRITE_SOS_TYPE = 'Sequential DCT'

        with open(tempfile.name, 'r') as tfile:
            with open(PROCESS14_O1_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

    def test_parse_o2(self):
        """Test that parsing the O2 file produces the correct output."""
        COMMON.WRITE_SOS_DATA = True
        COMMON.WRITE_SOS_TYPE = 'Lossless'

        with open(PROCESS14_O2, 'rb') as fp:
            info = parse_jpg(fp)
            file_length = fp.tell()

        # Order by offset
        keys = sorted(info.keys(), key=lambda x: int(x.split('@')[1]))

        tempfile = NamedTemporaryFile()
        with open(tempfile.name, 'w') as tfile:
            tfile.write(
                "Parser output for 'testo2.jpg', May 11, 1994, "
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
            COMMON.WRITE_SOS_TYPE = 'Sequential DCT'

        with open(tempfile.name, 'r') as tfile:
            with open(PROCESS14_O2_REF, 'r', encoding='utf-8', errors='ignore') as rfile:
                for out, ref in zip(tfile, rfile):
                    assert ref == out

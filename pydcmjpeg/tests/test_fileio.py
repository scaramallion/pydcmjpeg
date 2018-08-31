"""Tests for pydcmjpeg.fileio module."""

import os

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


class TestJPGRead(object):
    def setup(self):
        """"""
        pass

    def test_environment(self):
        """Test that the environment is as expected."""
        assert os.path.exists(C10918_PROCESS01)
        assert os.path.exists(C10918_PROCESS02)
        assert os.path.exists(C10918_PROCESS04)
        assert os.path.exists(C10918_PROCESS14)

    def test_open_filelike(self):
        """Test that we can open the file-like."""
        jpgread(PROCESS01_B2)


class TestJPEGWrite(object):
    pass

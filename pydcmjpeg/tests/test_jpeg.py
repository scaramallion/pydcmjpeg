"""Tests for the jpeg.JPEG class."""

import pytest

from pydcmjpeg import jpgread

from ._common import REFERENCE_DATA


class TestJPEG(object):
    """"""
    @pytest.mark.parametrize("fpath,data", REFERENCE_DATA['p1'])
    def test_process1(self, fpath, data):
        """Test that the right process type is returned."""
        jpg = jpgread(fpath)
        assert jpg.is_process1
        assert not jpg.is_process2
        assert not jpg.is_process4
        #assert not jpg.is_process14
        assert not jpg.is_process14_sv1

        assert jpg.precision == 8
        assert jpg.is_baseline
        assert not jpg.is_lossless
        assert jpg.is_non_hierarchical
        assert not jpg.is_hierarchical
        assert jpg.uid == '1.2.840.10008.1.2.4.50'

    @pytest.mark.parametrize("fpath,data", REFERENCE_DATA['p2'])
    def test_process2(self, fpath, data):
        """Test that the right process type is returned."""
        jpg = jpgread(fpath)
        assert not jpg.is_process1
        assert jpg.is_process2
        assert not jpg.is_process4
        #assert not jpg.is_process14
        assert not jpg.is_process14_sv1

        assert jpg.precision == 8
        assert jpg.is_extended
        assert not jpg.is_lossless
        assert jpg.is_non_hierarchical
        assert not jpg.is_hierarchical
        assert jpg.uid == '1.2.840.10008.1.2.4.51'

    @pytest.mark.parametrize("fpath,data", REFERENCE_DATA['p4'])
    def test_process4(self, fpath, data):
        """Test that the right process type is returned."""
        jpg = jpgread(fpath)
        assert not jpg.is_process1
        assert not jpg.is_process2
        assert jpg.is_process4
        #assert not jpg.is_process14
        assert not jpg.is_process14_sv1

        assert jpg.precision == 12
        assert jpg.is_extended
        assert not jpg.is_lossless
        assert jpg.is_non_hierarchical
        assert not jpg.is_hierarchical
        assert jpg.uid == '1.2.840.10008.1.2.4.51'

    @pytest.mark.parametrize("fpath,data", REFERENCE_DATA['p14'])
    def test_process14(self, fpath, data):
        """Test that the right process type is returned."""
        pass

    @pytest.mark.parametrize("fpath,data", REFERENCE_DATA['p14sv1'])
    def test_process14sv1(self, fpath, data):
        """Test that the right process type is returned."""
        jpg = jpgread(fpath)
        assert not jpg.is_process1
        assert not jpg.is_process2
        assert not jpg.is_process4
        #assert not jpg.is_process14
        assert jpg.is_process14_sv1

        #assert jpg.precision == 12
        assert jpg.is_extended
        assert jpg.is_lossless
        assert jpg.is_non_hierarchical
        assert not jpg.is_hierarchical
        assert jpg.uid == '1.2.840.10008.1.2.4.70'


class TestJPEG_Process1(object):
    """"""
    def test_uid(self):
        pass

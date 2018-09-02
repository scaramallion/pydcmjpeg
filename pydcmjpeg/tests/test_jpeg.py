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

        if data:
            assert data[0] == jpg.rows
            assert data[1] == jpg.columns
            assert data[2] == jpg.samples
            assert data[3] == jpg.precision

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

        if data:
            assert data[0] == jpg.rows
            assert data[1] == jpg.columns
            assert data[2] == jpg.samples
            assert data[3] == jpg.precision

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

        if data:
            assert data[0] == jpg.rows
            assert data[1] == jpg.columns
            assert data[2] == jpg.samples
            assert data[3] == jpg.precision

    @pytest.mark.parametrize("fpath,data", REFERENCE_DATA['p14'])
    def test_process14(self, fpath, data):
        """Test that the right process type is returned."""
        if data:
            assert data[0] == jpg.rows
            assert data[1] == jpg.columns
            assert data[2] == jpg.samples
            assert data[3] == jpg.precision

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
        assert not jpg.is_extended
        assert jpg.is_lossless
        assert jpg.is_non_hierarchical
        assert not jpg.is_hierarchical
        assert jpg.uid == '1.2.840.10008.1.2.4.70'

        if data:
            assert data[0] == jpg.rows
            assert data[1] == jpg.columns
            assert data[2] == jpg.samples
            assert data[3] == jpg.precision

    def test_get_keys(self):
        """Test JPEG.get_keys."""
        jpg = jpgread(REFERENCE_DATA['p1'][1][0])
        assert ['SOI@0'] == jpg.get_keys('SOI')
        assert ['SOF0@395'] == jpg.get_keys('SOF')
        assert len(jpg.get_keys('SOS')) == 255
        assert [] == jpg.get_keys('XXX')


class TestJPEGDecode(object):
    """Tests for JPEG.decode()."""
    def setup(self):
        """Setup the test datasets."""
        self.p1a = REFERENCE_DATA['p1'][0][0]
        self.p1d = REFERENCE_DATA['p1'][4][0]

    def test_decode_process1(self):
        """Decode a process 1 JPG."""
        jpg = jpgread(self.p1d)
        arr = jpg.to_array
        #assert (8, 16, 3) == arr.shape
        #assert 'uint8' == arr.dtype

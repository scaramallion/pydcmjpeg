"""Tests for the pydcmjpeg.utils module."""

import pytest

from pydcmjpeg.utils import get_specification


class TestGetSpecification_10918(object):
    """Tests for the utils.get_specification function."""
    def test_sof_00(self):
        pass

    def test_sof_01(self):
        pass

    def test_sof_03(self):
        pass

    def test_unsupported_sof_raises(self):
        pass

    def test_no_sof_raises(self):
        pass

    def test_not_jpeg_raises(self):
        pass


class TestGetSpecification_14495(object):
    """Tests for the utils.get_specification function."""
    def test_unsupported_sof_raises(self):
        pass


class TestGetSpecification_15444(object):
    """Tests for the utils.get_specification function."""
    def test_unsupported_raises(self):
        pass

"""Compliance tests for 14495."""

import os
from tempfile import NamedTemporaryFile

import pytest

from pydcmjpeg._markers import MARKERS
from pydcmjpeg.fileio import jpgread, parse_jpg

from ._common import WRITERS


COMPL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../', '../', 'data', 'compliance')
)

C14495 = os.path.join(COMPL_DIR, '14495', 'jlsimgV100')

# 8-bit, colour mode 0, lossless
T8C0E0 = os.path.join(C14495, 'T8C0E0.JLS')
# 8-bit, colour mode 0, near-lossless
T8C0E3 = os.path.join(C14495, 'T8C0E3.JLS')
# 8-bit, colour mode 1, lossless
T8C1E0 = os.path.join(C14495, 'T8C1E0.JLS')
# 8-bit, colour mode 1, near-lossless
T8C1E3 = os.path.join(C14495, 'T8C1E3.JLS')
# 8-bit, colour mode 2, lossless
T8C2E0 = os.path.join(C14495, 'T8C2E0.JLS')
# 8-bit, colour mode 2, near-lossless
T8C2E3 = os.path.join(C14495, 'T8C2E3.JLS')
# 8-bit, line interleaved, lossless, T1=T2=T3=9, RESET=31
T8NDE0 = os.path.join(C14495, 'T8NDE0.JLS')
# 8-bit, line interleaved, near-lossless, T1=T2=T3=9, RESET=31
T8NDE3 = os.path.join(C14495, 'T8NDE3.JLS')
# 8-bit, line-interleaved, lossless, R not subsampled, G subsampled 4x vert,
#  B subsampled 2x hor and vert
T8SSE0 = os.path.join(C14495, 'T8SSE0.JLS')
# 8-bit, line-interleaved, near-lossless, R not subsampled, G subsampled 4x vert,
#  B subsampled 2x hor and vert
T8SSE3 = os.path.join(C14495, 'T8SSE3.JLS')
# 16-bit, lossless
T16E0 = os.path.join(C14495, 'T16E0.JLS')
# 16-bit, near-lossless
T16E3 = os.path.join(C14495, 'T16E3.JLS')


class TestJPEGLS_ParseLossless(object):
    def test_parse_T8C0E0(self):
        jpg = jpgread(T8C0E0)

    def test_parse_T8C1E0(self):
        jpg = jpgread(T8C1E0)

    def test_parse_T8C2E0(self):
        jpg = jpgread(T8C2E0)

    def test_parse_T8NDE0(self):
        jpg = jpgread(T8NDE0)

    def test_parse_T8SSE0(self):
        jpg = jpgread(T8SSE0)

    def test_parse_T16E0(self):
        jpg = jpgread(T16E0)


class TestJPEGLS_ParseNearLossless(object):
    def test_parse_T8C0E3(self):
        jpg = jpgread(T8C0E3)

    def test_parse_T8C1E3(self):
        jpg = jpgread(T8C1E3)

    def test_parse_T8C2E3(self):
        jpg = jpgread(T8C2E3)

    def test_parse_T8NDE3(self):
        jpg = jpgread(T8NDE3)

    def test_parse_T8SSE3(self):
        jpg = jpgread(T8SSE3)

    def test_parse_T16E3(self):
        jpg = jpgread(T16E3)

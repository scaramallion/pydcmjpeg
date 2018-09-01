
from pydcmjpeg.config import JPEG_10918

class JPEG(object):
    """A representation of an ISO/IEC 10918-1 JPEG file."""
    def __init__(self, fp, info):
        self._fp = fp
        self.info = info
        self._array = None
        self._array_id = None

    @property
    def is_baseline(self):
        raise NotImplementedError

    @property
    def is_sequential(self):
        raise NotImplementedError

    @property
    def is_huffman(self):
        raise NotImplementedError

    @property
    def is_arithmetic(self):
        raise NotImplementedError

    @property
    def is_extended(self):
        raise NotImplementedError

    @property
    def is_progressive(self):
        raise NotImplementedError

    @property
    def is_lossless(self):
        raise NotImplementedError

    @property
    def is_parsable(self):
        raise True

    @property
    def is_decodable(self):
        return False

    @property
    def uid(self):
        raise NotImplementedError

    @property
    def is_process1(self):
        raise NotImplementedError

    @property
    def is_process2(self):
        raise NotImplementedError

    @property
    def is_process4(self):
        raise NotImplementedError

    @property
    def is_process14(self):
        raise NotImplementedError

    @property
    def is_process14_sv1(self):
        raise NotImplementedError

    @property
    def to_array(self):
        raise NotImplementedError

    @property
    def to_bytes(self):
        raise NotImplementedError

    def from_array(self, arr):
        raise NotImplementedError

    def decode(self):
        raise NotImplementedError


class JPEGBase(object):
    """Base class for representing a JPEG file."""
    def __init__(self, fp):
        # The file-like that contains the JPEG file
        self._fp = fp
        self.info = {}

    def parse(self):
        pass


class JPEGLS(object):
    """A representation of an ISO/IEC 14495-1 JPEG-LS file."""
    def __init__(self):
        raise NotImplementedError('JPEG-LS is not supported')


class JPEG2000(object):
    """A representation of an ISO/IEC 15444-1 JPEG 2000 file."""
    def __init__(self):
        raise NotImplementedError('JPEG 2000 is not supported')


def get_jpeg(fp, info):
    """Return a class representing the JPEG file."""
    # JPEG 10918 uses the following SOF markers
    # 0 to 3, 5 to 7, 9 to 11, 13 to 15
    markers = [key.split('@')[0] for key in info]
    is_10918_jpg = set(JPEG_10918).intersection(markers)

    if is_10918_jpg:
        return JPEG(fp, info)
    else:
        raise NotImplementedError(
            "The JPEG file is not supported"
        )

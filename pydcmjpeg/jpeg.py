

class JPEG(object):
    """A representation of an ISO/IEC 10918-1 JPEG file.

    Only JPEG Processes 1, 2, 4 and 14 are supported.
    """
    pass

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
    raise NotImplementedError('JPEG-LS is not supported')


class JPEG2000(object):
    """A representation of an ISO/IEC 15444-1 JPEG 2000 file."""
    raise NotImplementedError('JPEG 2000 is not supported')

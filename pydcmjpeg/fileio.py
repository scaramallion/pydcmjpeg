""""""

import logging

from pydcmjpeg.config import PARSE_SUPPORTED
from pydcmjpeg.jpeg import get_jpeg
from pydcmjpeg.utils import get_specification


LOGGER = logging.getLogger('pdcmjpeg')


def jpgread(fpath):
    """Return a represention of the JPEG file at `fpath`."""
    LOGGER.debug("Reading file: {}".format(fpath))
    with open(fpath, 'rb') as fp:
        info = parse_jpeg(fp)
        LOGGER.debug("File parsed successfully")

        return get_jpeg(info)


def jpgwrite(fpath, jpg):
    """Write the JPEG object `jpg` to `fpath`."""
    raise NotImplementedError('Writing JPEG files is not supported')


def parse_jpeg(fp):
    """Return a JPEG but don't decode yet."""
    jpeg = JPEGBase(fp)

    if fp.read(1) != b'\xff':
        raise ValueError('File is not JPEG')

    fp.seek(-1, 1)

    info = {}

    while True:
        _marker = unpack('>H', fp.read(2))[0]

        if _marker in MARKERS:
            if _marker != 0xFFDA:
                name, description, handler = MARKERS[_marker]
                print(
                    "{0} @ offset {1} : {2} : {3}"
                    .format(hex(_marker), fp.tell() - 2, name, description)
                )

                if handler is None:
                    length = unpack('>H', fp.read(2))[0] - 2
                    fp.seek(length, 1)
                else:
                    info[name] = handler(fp)
            else:
                # SOS - start of scan
                name, description, handler = MARKERS[_marker]
                print(
                    "{0} @ offset {1} : {2} : {3}"
                    .format(hex(_marker), fp.tell() - 2, name, description)
                )
                handler(fp)
                break
                # decode ecs
        else:
            print('Unknown marker {0} at offset {1}'
                  .format(hex(_marker), fp.tell() - 2))
            raise NotImplementedError

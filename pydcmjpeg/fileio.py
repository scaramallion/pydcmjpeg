""""""

import logging
from struct import unpack

from pydcmjpeg._markers import MARKERS
from pydcmjpeg.jpeg import get_jpeg
from pydcmjpeg.utils import get_specification


LOGGER = logging.getLogger('pdcmjpeg')


def jpgread(fpath):
    """Return a represention of the JPEG file at `fpath`."""
    LOGGER.debug("Reading file: {}".format(fpath))
    with open(fpath, 'rb') as fp:
        info = parse_jpeg(fp)
        LOGGER.debug("File parsed successfully")

        return get_jpeg(fp, info)


def jpgwrite(fpath, jpg):
    """Write the JPEG object `jpg` to `fpath`."""
    raise NotImplementedError('Writing JPEG files is not supported')


def parse_jpeg(fp):
    """Return a JPEG but don't decode yet."""
    # Passing 10918-2 Process 1 compliance tests
    if fp.read(1) != b'\xff':
        fp.seek(0)
        raise ValueError('File is not JPEG')

    while fp.read(1) == b'\xff':
        pass

    fp.seek(-2, 1)

    # Confirm SOI marker
    if fp.read(2) != b'\xFF\xD8':
        raise ValueError('SOI marker not found')

    fp.seek(-2, 1)

    info = {}

    while True:

        # Skip fill
        next_byte = fp.read(1)
        while next_byte == b'\xFF':
            next_byte = fp.read(1)

        fp.seek(-2, 1)

        _marker = unpack('>H', fp.read(2))[0]

        if _marker in MARKERS:
            if _marker not in [0xFFDA, 0xFFD9]:
                name, description, handler = MARKERS[_marker]
                print(
                    "{1}   {2} ({0})"
                    .format(hex(_marker), fp.tell() - 2, name)
                )

                if handler is None:
                    length = unpack('>H', fp.read(2))[0] - 2
                    fp.seek(length, 1)
                else:
                    info[name] = handler(fp)
            elif _marker == 0xFFDA:
                # SOS - start of scan
                name, description, handler = MARKERS[_marker]
                print(
                    "{1}   {2} ({0})"
                    .format(hex(_marker), fp.tell() - 2, name)
                )
                handler(fp)

                # Skip ECS and all the 0xFF00 that may occur
                while True:
                    next_byte = fp.read(1)
                    if next_byte != b'\xFF':
                        # BP = BP + 1
                        continue

                    next_byte = fp.read(1)
                    if next_byte == b'\x00':
                        continue

                    fill_bytes = 0
                    while next_byte == b'\xFF':
                        fill_bytes += 1
                        next_byte = fp.read(1)

                    if fill_bytes:
                        print('  {} FIL bytes'.format(fill_bytes))

                    # Check RST_m
                    if next_byte in [b'\xD0', b'\xD1', b'\xD2', b'\xD3',
                                     b'\xD4', b'\xD5', b'\xD6', b'\xD7']:
                        continue

                    fp.seek(-2, 1)
                    break

            elif _marker == 0xFFD9:
                name, description, handler = MARKERS[_marker]
                print(
                    "{1}   {2} ({0})"
                    .format(hex(_marker), fp.tell() - 2, name)
                )
                break

        else:
            print('Unknown marker {0} at offset {1}'
                  .format(hex(_marker), fp.tell() - 2))
            raise NotImplementedError

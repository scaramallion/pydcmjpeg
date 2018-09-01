""""""

import logging
from struct import unpack

from pydcmjpeg._markers import MARKERS
from pydcmjpeg.jpeg import get_jpeg


LOGGER = logging.getLogger('pdcmjpeg')


def jpgread(fpath):
    """Return a represention of the JPEG file at `fpath`."""
    LOGGER.debug("Reading file: {}".format(fpath))
    with open(fpath, 'rb') as fp:
        info = parse_jpg(fp)
        LOGGER.debug("File parsed successfully")

        return get_jpeg(fp, info)


def jpgwrite(fpath, jpg):
    """Write the JPEG object `jpg` to `fpath`."""
    raise NotImplementedError('Writing JPEG files is not supported')


def _marker_key(name, offset):
    """Return a string combining `name` and `offset`"""
    return '{0}@{1}'.format(name, offset - 2)


def parse_jpg(fp):
    """Return a JPEG but don't decode yet."""
    # Passing 10918-2 Process 1 compliance tests
    if fp.read(1) != b'\xff':
        fp.seek(0)
        raise ValueError('File is not JPEG')

    _fill_bytes = 0
    while fp.read(1) == b'\xff':
        _fill_bytes += 1
        pass

    #if _fill_bytes == 1:
    #    _fill_bytes = 0

    fp.seek(-2, 1)

    # Confirm SOI marker
    if fp.read(2) != b'\xFF\xD8':
        raise ValueError('SOI marker not found')

    info = {
        _marker_key('SOI', fp.tell()) : (unpack('>H', b'\xFF\xD8')[0], _fill_bytes, {})
    }

    while True:
        _fill_bytes = 0

        # Skip fill
        next_byte = fp.read(1)
        while next_byte == b'\xFF':
            _fill_bytes += 1
            next_byte = fp.read(1)

        # Remove the byte thats actually part of the marker
        if _fill_bytes:
            _fill_bytes -= 1

        fp.seek(-2, 1)

        _marker = unpack('>H', fp.read(2))[0]

        if _marker in MARKERS:
            name, description, handler = MARKERS[_marker]
            key = _marker_key(name, fp.tell())
            if name not in ['SOS', 'EOI']:
                if handler is None:
                    length = unpack('>H', fp.read(2))[0] - 2
                    fp.seek(length, 1)
                    continue

                info[key] = (_marker, _fill_bytes , handler(fp))

            elif name is 'SOS':
                info[key] = (_marker, _fill_bytes, handler(fp))

                # Skip ECS and all the 0xFF00 that may occur
                while True:
                    next_byte = fp.read(1)
                    if next_byte != b'\xFF':
                        continue

                    next_byte = fp.read(1)
                    if next_byte == b'\x00':
                        continue

                    # The number of 0xFF bytes before the marker
                    #   i.e. 0xFF 0xFF 0xFF 0xD9 is 2 fill bytes
                    _fill_bytes = 0
                    # While we still have 0xFF bytes
                    while next_byte == b'\xFF':
                        _fill_bytes += 1
                        next_byte = fp.read(1)

                    #if _fill_bytes:
                    #    print('  {} FIL bytes'.format(_fill_bytes))

                    # Check RST_m
                    if next_byte in [b'\xD0', b'\xD1', b'\xD2', b'\xD3',
                                     b'\xD4', b'\xD5', b'\xD6', b'\xD7']:
                        continue

                    # Back up to the start of the 0xFF
                    # Currently position at first byte after marker
                    fp.seek(-2 - _fill_bytes, 1)
                    break

            elif name is 'EOI':
                info[key] = (_marker, _fill_bytes, {})
                break

        else:
            print('Unknown marker {0} at offset {1}'
                  .format(hex(_marker), fp.tell() - 2))
            raise NotImplementedError

    return info

""""""

import logging
import mmap
from struct import unpack

from pydcmjpeg._markers import MARKERS
from pydcmjpeg.jpeg import get_jpeg


LOGGER = logging.getLogger('pdcmjpeg')


def jpgmap(fpath):
    """Return a memory-mapped representation of the JPEG file at `fpath`."""
    LOGGER.debug('Mapping file: {}'.format(fpath))
    with open(fpath, 'r+b') as fp:
        # Size 0 means whole file
        mm = mmap.mmap(fp.fileno(), 0)
        return JPEGDict(map_jpg(mm))


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


def map_jpg(mm):
    pass


def parse_jpg(fp):
    """Return a JPEG but don't decode yet."""
    # Passing 10918-2 Process 1 compliance tests
    if fp.read(1) != b'\xff':
        fp.seek(0)
        raise ValueError('File is not JPEG')

    JPEG_TYPE = 'JPEG'

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
            #print(hex(_marker), name, fp.tell() - 2)
            key = _marker_key(name, fp.tell())
            if name not in ['SOS', 'EOI', 'LSE']:
                if handler is None:
                    #length = unpack('>H', fp.read(2))[0] - 2
                    #fp.seek(length, 1)
                    fp.seek(2, 1)
                    continue

                info[key] = (_marker, _fill_bytes , handler(fp))
                #print(info[key])

            elif name is 'SOS':
                # SOS's info dict contains an extra 'encoded_data' keys
                # which use RSTN@offset and ENC@offset

                for kk in info:
                    if 'SOF55' in kk:
                        JPEG_TYPE = 'JPEG-LS'
                        break
                info[key] = [_marker, _fill_bytes, handler(fp, jpg=JPEG_TYPE)]
                #print(info[key])

                sos_info = {}
                encoded_data = bytearray()
                _enc_start = fp.tell()

                while True:
                    _enc_key = _marker_key('ENC', _enc_start)
                    prev_byte = fp.read(1)
                    if prev_byte != b'\xFF':
                        encoded_data.extend(prev_byte)
                        continue

                    # To get here next_byte must be 0xFF
                    # If the next byte is 0x00 then keep reading
                    # JPEGLS: if the next bit is 0, discard the inserted bit
                    #         if the next bit is 1, then is a marker
                    # If the next byte is 0xFF then keep reading until
                    #   a non-0xFF byte is found
                    # If the marker is a RST marker then keep reading
                    # Otherwise rewind to the start of the fill bytes and break

                    next_byte = fp.read(1)
                    if JPEG_TYPE == 'JPEG':
                        if next_byte == b'\x00':
                            # Skip padding bytes
                            # The previous byte wasn't added so do it now
                            encoded_data.extend(prev_byte)
                            #encoded_data.extend(next_byte)
                            continue
                    elif JPEG_TYPE == 'JPEG-LS':
                        encoded_data.extend(prev_byte)
                        encoded_data.extend(next_byte)
                        next_byte = unpack('B', next_byte)[0]
                        #print('nb', next_byte, bin(next_byte))
                        #print('{:>08b}'.format(next_byte))
                        #print('{:>08b}'.format(next_byte)[0])
                        #print('{:>08b}'.format(next_byte)[0] == '0')

                        if '{:>08b}'.format(next_byte)[0] == '0':
                            #print('MSB is 0')
                            continue

                    # To get here next_byte must be non-padding (non 0x00)
                    #   so we must be at the end of the encoded data

                    info[key][2].update({_enc_key : encoded_data})
                    encoded_data = bytearray()

                    # The number of 0xFF bytes before the marker
                    #   i.e. 0xFF 0xFF 0xFF 0xD9 is 2 fill bytes
                    _sos_fill_bytes = 0
                    # While we still have 0xFF bytes
                    while next_byte == b'\xFF':
                        _sos_fill_bytes += 1
                        next_byte = fp.read(1)

                    # Check to see if marker is RST_m
                    if next_byte in [b'\xD0', b'\xD1', b'\xD2', b'\xD3',
                                     b'\xD4', b'\xD5', b'\xD6', b'\xD7']:
                        _sos_marker = unpack('>H', b'\xFF' + next_byte)[0]
                        _sos_marker, _, _ = MARKERS[_sos_marker]
                        _sos_key = _marker_key(_sos_marker, fp.tell())
                        info[key][2].update({_sos_key : None})

                        _enc_start = fp.tell()
                        continue

                    # End of the current scan, rewind and break
                    # Back up to the start of the 0xFF
                    # Currently position at first byte after marker
                    fp.seek(-2 - _sos_fill_bytes, 1)
                    break

            elif name is 'EOI':
                info[key] = (_marker, _fill_bytes, {})
                break

            elif name is 'LSE':
                # JPEG-LS
                info[key] = (_marker, _fill_bytes, handler(fp, info))

        else:
            print('Unknown marker {0} at offset {1}'
                  .format(hex(_marker), fp.tell() - 2))
            raise NotImplementedError

    return info

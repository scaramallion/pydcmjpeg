#!/usr/bin/env python
"""An application for dumping information about a JPEG file."""

import argparse
from struct import unpack

from pyjpeg._markers import MARKERS


def setup_argparse():
    pass


if __name__ == "__main__":
    fpath = '../tests/huff_simple0.jpg'

    with open(fpath, 'rb') as fp:
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
                        "{0} @ {1} : {2} {3}"
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
                        "{0} @ {1} : {2} {3}"
                        .format(hex(_marker), fp.tell() - 2, name, description)
                    )
                    handler(fp)
                    print('Decoding ECS...')
                    break
                    # decode ecs
            else:
                print('Unknown marker {0} at offset {1}'
                      .format(hex(_marker), fp.tell() - 2))
                raise NotImplementedError

        print(info)

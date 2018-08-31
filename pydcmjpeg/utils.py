

from pydcmjpeg._markers import MARKERS


def get_specification(fp):
    """
    Supported ISO/IEC standards are 10918, 14495, 15444.

    Probably needs to be made more precise.

    Parameters
    ----------
    fp : file-like

    Returns
    -------
    tuple of str
        The (ISO/IEC standard, jpeg specification).
    """
    standard = None
    specification = None

    _marker = unpack('>H', fp.read(2))[0]

    if _marker not in [0xFFD8, 0xFF4F]:
        # Play nice and rewind
        fp.seek(0)
        raise ValueError('File is not JPEG or not supported')

    if _marker == 0xFF4F:
        standard = '15444'

    _continue_parsing = True
    while _continue_parsing:
        _marker = unpack('>H', fp.read(2))[0]
        if _marker not in MARKERS:
            fp.seek(0)
            raise NotImplementedError(
                'Unknown marker {0} at offset {1}'
                .format(hex(_marker), fp.tell() - 2)
            )

        # Start of Scan (SOS) or End of Image (EOI) markers
        if _marker in [0xFFDA, 0xFFD9]:
            _continue_parsing = False
            break

        # We are looking for a SOF_NN marker for 10918/14495
        name, description, handler = MARKERS[_marker]
        if name in ['SOF_0', 'SOF_1', 'SOF_3']:
            standard = '10918'
            specification = name
            break

        # Skip ahead to the next marker
        if handler is None:
            length = unpack('>H', fp.read(2))[0] - 2
            fp.seek(length, 1)
        else:
            handler(fp)

    if not standard or not specification:
        fp.seek(0)
        raise ValueError('Unable to determine the JPEG specification')

    fp.seek(0)

    return (standard, specification)

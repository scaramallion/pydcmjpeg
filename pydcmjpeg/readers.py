"""
For parameters which are 2 bytes, the most significant byte shall come first
in the compressed data's ordered sequence of bytes. Parameters which are 4
bits in length always come in pairs and the pair shall always be encoded as
a single byte. The first 4-bit parameter of the pair shall occupy the most
significant 4 bits of the byte. Within and 16-, 8- or 4-bit parameter the
MSB shall come first and the LSB shall come last.

BIG ENDIAN.

Non-hierarchical

SOI | Frame | EOI

Frame
[Tables/misc] | SOF Frame header | Scan_1 | [DNL segment] | [Scan_2] ... | [Scan_n] |

Scan
[Tables/misc] | Scan header | [ECS_0 | RST_0 | ... | RST_n] | ECS_n |

ECS
<MCU1>, <MCU_2>, ..., <MCU_R>
"""

from struct import unpack



def _split_byte(bs):
    """Split the 8-bit byte `bs` into two 4-bit integers."""
    mask_msb = 0b11110000
    mask_lsb = 0b00001111

    return (mask_msb & bs[0]) >> 4, mask_lsb & bs[0]


def _get_bit(byte, ii):
    """Return the bit value at index `ii` of `byte`.

    Bit index is 0 = MSB, 7 = LSB
    """
    return (byte >> (7 - ii)) & 1


def APP(fp):
    """Parse an APP_n maker segment.

    APP_n - Application data marker
    Lp - Application data segment length
    Ap - Application data
    """
    length = unpack('>H', fp.read(2))[0]

    info = {
        'Lp' : length,
        'Ap' : fp.read(length - 2)
    }

    return info


def COC(fp, csiz):
    """Parse a COC marker segment."""
    lcoc = unpack('>H', fp.read(2))[0]
    print('Csiz', csiz)
    if csiz < 257:
        ccoc = unpack('B', fp.read(1))[0]
    else:
        ccoc = unpack('>H', fp.read(2))[0]
    scoc = unpack('B', fp.read(1))[0]

    _decomp_levels = unpack('B', fp.read(1))[0]
    _block_width = unpack('B', fp.read(1))[0]
    _block_height = unpack('B', fp.read(1))[0]
    _block_style = unpack('B', fp.read(1))[0]
    _transform = unpack('B', fp.read(1))[0]

    _precincts = []
    has_precincts = _get_bit(scoc, 7)
    if has_precincts == 1:
        for ii in range(_decomp_levels + 1):
            _precincts.append(unpack('B', fp.read(1))[0])

    info = {
        'Lcoc' : lcoc,
        'Ccoc' : ccoc,
        'Scoc' : scoc,
        'SPcoc' : {
            'decomp_levels' : _decomp_levels,
            'block_width' : _block_width,
            'block_height' : _block_height,
            'block_style' : _block_style,
            'transform' : _transform
        }
    }

    if has_precincts:
        info['SPcoc']['precincts'] = _precincts

    return info


def COD(fp):
    """Parse a COD marker segment."""
    lcod = unpack('>H', fp.read(2))[0]
    scod = unpack('B', fp.read(1))[0]
    sgcod = {
        'progression_order' : unpack('B', fp.read(1))[0],
        'nr_layers' : unpack('>H', fp.read(2))[0],
        'mc_transform' : unpack('B', fp.read(1))[0],
    }

    # SPcod
    _decomp_levels = unpack('B', fp.read(1))[0]
    _block_width = unpack('B', fp.read(1))[0]
    _block_height = unpack('B', fp.read(1))[0]
    _block_style = unpack('B', fp.read(1))[0]
    _transform = unpack('B', fp.read(1))[0]

    _precincts = []
    has_precincts = _get_bit(scod, 7)
    if has_precincts == 1:
        for ii in range(_decomp_levels + 1):
            _precincts.append(unpack('B', fp.read(1))[0])

    info = {
        'Lcod' : lcod,
        'Scod' : scod,
        'SGcod' : sgcod,
        'SPcod' : {
            'decomp_levels' : _decomp_levels,
            'block_width' : _block_width,
            'block_height' : _block_height,
            'block_style' : _block_style,
            'transform' : _transform
        }
    }

    if has_precincts:
        info['SPcod']['precincts'] = _precincts

    return info


def COM(fp):
    """Parse a COM marker segment.

    COM - Comment marker
    Lc - Comment segment length
    Cm - Comment bytes.
    """
    length = unpack('>H', fp.read(2))[0]
    comment = unpack('{}s'.format(length - 2), fp.read(length - 2))[0]

    info = {
        'Lc' : length,
        'Cm' : comment
    }

    return info


def COM_JP2(fp):
    """Parse a JP2K COM marker segment"""
    lcom = unpack('>H', fp.read(2))[0]
    rcom = unpack('>H', fp.read(2))[0]
    ccom = unpack('{}s'.format(lcom - 4), fp.read(lcom - 4))[0]

    info = {
        'Lcom' : lcom,
        'Rcom' : rcom,
        'Ccom' : ccom,
    }

    return info


def DAC(fp):
    """Parse a DAC marker segment.

    DAC - Define arithmetic coding conditioning marker
    La - Arithmetic coding conditioning length
    Tc - Table class 0 = DC or lossless, 1 = AC
    Tb - Arithmetic coding conditioning table destination identifier
    Cs - Conditioning table value
    """
    length = unpack('>H', fp.read(2))[0]
    _remaining = length - 2

    _tc, _tb, _cs = [], [], []
    while _remaining:
        tc, tb = _split_byte(fp.read(1))
        _cs.append(unpack('>B', fp.read(1))[0])
        _remaining -= 2
        _tc.append(tc)
        _tb.append(tb)

    info = {
        'La' : length,
        'Tc' : _tc,
        'Tb' : _tb,
        'Cs' : _cs
    }

    return info


def DHT(fp):
    """Parse a DHT marker segment.

    DHT - Define Huffman table marker
    Lh - Huffmn table definition length
    Tc - Table class 0 = DC or lossless, 1 = AC
    Th - Huffman table destination identifier, one of four possible
         destinations at the decoder into which the table shall be installed
    Li - Number of Huffman codes of length i, BITS
    Vij - Value associated with each Huffman code of length i, equivalent to
          HUFFVAL
    """
    length = unpack('>H', fp.read(2))[0]
    _remaining = length - 2

    _tc, _th = [], []
    _li = []
    _vij = []
    while _remaining > 0:
        tc, th = _split_byte(fp.read(1))
        _tc.append(tc)
        _th.append(th)
        _remaining -= 1

        # li (BITS) is the number of codes for each code length, from 1 to 16
        li = unpack('>16B', fp.read(16))
        _remaining -= 16
        # vij is a list of the 8-bit symbols values (HUFFVAL), each of which
        #   is assigned a Huffman code.
        vij = []
        for nr in li:
            if nr:
                vij.append(unpack('>{}B'.format(nr), fp.read(nr)))
                _remaining -= nr
            else:
                vij.append(None)

        _li.append(li)
        _vij.append(vij)

    info = {
        'Lh' : length,
        'Tc' : _tc,
        'Th' : _th,
        'Li' : _li,
        'Vij' : _vij,
    }

    return info


def DNL(fp):
    """Parse a DNL marker segment.

    DNL - Define number of line marker
    Ld - Define number of lines segment length
    NL - Number of lines in the frame
    """
    length = unpack('>H', fp.read(2))[0]
    _nl = unpack('>H', fp.read(2))[0]

    info = {
        'Ld' : length,
        'NL' : _nl
    }

    return info


def DQT(fp):
    """Parse DQT marker segment.

    DQT - Define quantization table marker
    Lq - Quantization table definition length
    Pq - Quantization table element precision 0 = 8-bit, 1 = 16-bit
    Tq - Quantization table destination identifier
    Qk - Quantization table element
    """
    # length is 2 + sum(t=1, N) of (65 + 64 * Pq(t))
    length = unpack('>H', fp.read(2))[0]
    _remaining = length - 2

    _pq, _tq, _qk = [], [], []
    while _remaining > 0:
        precision, table_id = _split_byte(fp.read(1))
        _remaining -= 1
        _pq.append(precision)
        _tq.append(table_id)

        # If Pq is 0, Qk is 8-bit, if Pq is 1, Qk is 16-bit
        Q_k = []
        for ii in range(64):
            if precision == 0:
                Q_k.append(unpack('>B', fp.read(1))[0])
                _remaining -= 1
            elif precision == 1:
                Q_k.append(unpack('>H', fp.read(2))[0])
                _remaining -= 2

        _qk.append(Q_k)

    info = {
        'Lq' : length,
        'Pq' : _pq,
        'Tq' : _tq,
        'Qk' : _qk
    }

    return info


def DRI(fp):
    """Parse a DRI marker segment.

    DRI - Define restart interval marker
    Lr - Define restart interval segment length
    Ri - Restart interval (number of MCU in the restart interval)
    """
    info = {
        'Lr' : unpack('>H', fp.read(2))[0],
        'Ri' : unpack('>H', fp.read(2))[0]
    }

    return info


def EXP(fp):
    """Parse an EXP marker segment.

    EXP - Expand reference components marker
    Le - Expand reference components segment length
    Eh - Expand horizontally
    Ev - Expand vertically
    """
    length = unpack('>H', fp.read(2))[0]
    _eh, _ev = _split_byte(unpack('>B', fp.read(1))[0])

    info = {
        'Le' : length,
        'Eh' : _eh,
        'Ev' : _ev
    }

    return info


def LSE(fp, jpg_info):
    """Parse an LSE marker segment (JPEG-LS).

    LSE - JPEG-LS preset parameters marker
    Ll - Preset parameters length
    ID - parameter ID, specifies which JPEG-LS preset parameters follow
        ID: 0x01
            JPEG-LS preset coding parameters follow
            MAXVAL - The maximum possible value for any image sample in the
                     scan
            T1 - First quantization threshold for the local gradients
            T2 - Second quantization threshold for the local gradients
            T3 - Third quantization threshold for the local gradients
            RESET - Value at which the counters A, B and N are halved
        ID: 0x02
            A mapping table specification follows
            TID - Table ID
            Wt - Width of table entries in bytes
            TABLE - Sample mapping table
        ID: 0x03
            A mapping table continuation follows
            TABLE - The continuation of the mapping table
        ID: 0x04
            X and Y parameters greater than 16 bits are defined
            Wxy - number of bytes used to represent Ye and Xe
            Ye - number of lines in the image
            Xe - number of columns in the image
    """
    length = unpack('>H', fp.read(2))[0]
    _id = unpack('B', fp.read(1))[0]


    info = {
        'Ll' : length,
        'ID' : _id,
    }

    if _id == 1:
        info['MAXVAL'] = unpack('>H', fp.read(2))[0]
        info['T1'] = unpack('>H', fp.read(2))[0]
        info['T2'] = unpack('>H', fp.read(2))[0]
        info['T3'] = unpack('>H', fp.read(2))[0]
        info['RESET'] = unpack('>H', fp.read(2))[0]
    elif _id == 2:
        info['TID'] = unpack('>H', fp.read(1))[0]
        info['Wt'] = unpack('>H', fp.read(1))[0]
        info['TABLE'] = []

        if (5 + info['Wt'] * (info['MAXVAL'] + 1)) < 65535:
            MAXTAB = info['MAXVAL']
        else:
            MAXTAB = abs(65530 / info['Wt']) - 1
        for ii in range(MAXTAB):
            info['TABLE'].append(fp.read(info['Wt']))
    elif _id == 3:
        # Find most recent LSE entry prior to this one
        lse_keys = [kk for kk in jpg_info.keys() if kk.split('@')[0] == 'LSE']
        lse_keys = sorted(lse_keys, key=lambda x: int(x.split('@')[1]))
        most_recent = lse_keys[-1]

        entries = len(jpg_info[most_recent]['TABLE'])

        if (5 + info['Wt'] * (entries + 1)) < 65536:
            MAXTABX = entries - 1
        else:
            MAXTABX = abs(65530 / info['Wt']) - 1

        info['TID'] = jpg_info[most_recent]['TID']
        info['Wt'] = jpg_info[most_recent]['TID']
        info['TABLE'] = []
        for ii in range(MAXTABX):
            info['TABLE'].append(fp.read(info['Wt']))
    elif _id == 4:
        info['Wxy'] = unpack('>H', fp.read(1))[0]
        info['Ye'] = fp.read(info['Wxy'])
        info['Xe'] = fp.read(info['Wxy'])
        pass
    else:
        raise ValueError(
            'An LSE ID parameter value of {} is not valid'.format(ID)
        )

    return info


# FIXME
def QCC(fp, csiz):
    """Parse a QCC marker segment"""
    lqcc = unpack('>H', fp.read(2))[0]
    if csiz < 257:
        cqcc = unpack('B', fp.read(1))[0]
    else:
        cqcc = unpack('>H', fp.read(2))[0]

    sqcc = unpack('B', fp.read(1))[0]

    _spqcc = []

    info = {

    }

    return info


def QCD(fp):
    """Parse a QCD marker segment.


    """
    lqcd = unpack('>H', fp.read(2))[0]
    sqcd = unpack('B', fp.read(1))[0]

    _spqcd = []
    _remaining = lqcd - 3
    bitstring = '{:>08b}'.format(sqcd)
    while _remaining > 0:
        if bitstring[3:] == '00000':
            # xxx0 0000: no quantisation
            _spqcd.append(unpack('B', fp.read(1))[0])
            _remaining -= 1
        elif bitstring[3:] == '00001':
            # xxx0 0001: scalar derived
            _spqcd.append(unpack('>H', fp.read(2))[0])
            _remaining -= 2
        elif bitstring[3:] == '00010':
            # xxx0 0010: scalar expounded
            _spqcd.append(unpack('>H', fp.read(2))[0])
            _remaining -= 2
        else:
            raise NotImplementedError('QCD invalid value')

        #guard_bits = int(bitstring[3:], 2)

    info = {
        'Lqcd' : lqcd,
        'Sqcd' : sqcd,
        'SPqcd' : _spqcd
    }

    return info


def SIZ(fp):
    """Parse a SIZ marker segment

    SIZ - Image and tile size marker
    Lsiz - length of the marker segment
    Rsiz - capabilities a decoder needs
    Xsiz - width of the reference grid
    Ysiz - height of the reference grid
    XOsiz - horizontal offset from the origin of the reference grid
    YOsiz - vertical offset from the origin of the reference grid
    XTsiz - Width of one reference tile
    YTsiz - Height of one reference tile
    XTOsiz - Horizontal offset from the origin of the reference grid
    YTOsiz - Vertical offset from the origin of the reference grid
    Csiz - number of components in the image
    Ssiz - precision in bits and sign of the ith component samples
    XRsiz - horizontal separation of a sample of ith component
    YRsiz - vertical separation of a sample of ith component

    """
    info = {
        'Lsiz' : unpack('>H', fp.read(2))[0],
        'Rsiz' : unpack('>H', fp.read(2))[0],
        'Xsiz' : unpack('>L', fp.read(4))[0],
        'Ysiz' : unpack('>L', fp.read(4))[0],
        'XOsiz' : unpack('>L', fp.read(4))[0],
        'YOsiz' : unpack('>L', fp.read(4))[0],
        'XTsiz' : unpack('>L', fp.read(4))[0],
        'YTsiz' : unpack('>L', fp.read(4))[0],
        'XTOsiz' : unpack('>L', fp.read(4))[0],
        'YTOsiz' : unpack('>L', fp.read(4))[0],
        'Csiz' : unpack('>H', fp.read(2))[0],
    }

    _ssiz, _xrsiz, _yrsiz = [], [], []
    for ii in range(info['Csiz']):
        _ssiz.append(unpack('B', fp.read(1))[0])
        _xrsiz.append(unpack('B', fp.read(1))[0])
        _yrsiz.append(unpack('B', fp.read(1))[0])

    info['Ssiz'] = _ssiz
    info['XRsiz'] = _xrsiz
    info['YRsiz'] = _yrsiz

    return info


def SOD(fp):
    """Parse an SOD marker segment.

    SOD - Start of data segment 0xFF 0x93

    Last marker in a tile-part header. Bitstream data between a SOD and
    the next SOT or EOC shall be a multiple of 8 bits.
    """
    info = {}

    return info


def SOF(fp):
    """Read a SOF_NN 'Start of frame' header.

    +-----------+------+----------------------------------------------+
    | Parameter | Size | Values                                       |
    |           |      |---------------------+-------------+----------+
    |           | bits | Sequential          | Progressive | Lossless |
    |           |      +----------+----------+             |          |
    |           |      | Baseline | Extended |             |          |
    +===========+======+==========+==========+=============+==========+
    | Lf        | 16   |  8 + 3 * Nf                                  |
    +-----------+------+----------+----------+-------------+----------+
    | P         | 8    | 8        | 8, 12    | 8, 12       | 2-16     |
    +-----------+------+----------+----------+-------------+----------+
    | Y         | 16   | 0 - 65535                                    |
    +-----------+------+----------+----------+-------------+----------+
    | X         | 16   | 1 - 65535                                    |
    +-----------+------+----------+----------+-------------+----------+
    | Nf        | 8    | 1 - 255  | 1 - 255  | 1 - 4       | 1 - 255  |
    +-----------+------+----------+----------+-------------+----------+
    | Ci        | 8    | 0 - 255                                      |
    +-----------+------+----------+----------+-------------+----------+
    | Hi        | 4    | 1 - 4                                        |
    +-----------+------+----------+----------+-------------+----------+
    | Vi        | 4    | 1 - 4                                        |
    +-----------+------+----------+----------+-------------+----------+
    | Tqi       | 8    | 0 - 3    | 0 - 3    | 0 - 3       | 0        |
    +-----------+------+----------+----------+-------------+----------+

    SOF_n - Start if frame marker
    Lf - Frame header length
    P - Sample precision
    Y - Number of lines
    X - Number of samples per line
    Nf - Number of image components in frame
    Ci - Component identifier
    Hi - Horizontal sampling factor
    Vi - Vertical sampling factor
    Tqi - Quantization table destination selector
    """
    (length,
     precision,
     nr_lines,
     samples_per_line,
     nr_components) = unpack('>HBHHB', fp.read(8))

    component_id = []
    horizontal_sampling_factor = []
    vertical_sampling_factor = []
    quantisation_selector = []
    for ii in range(nr_components):
        _ci = unpack('>B', fp.read(1))[0]
        component_id.append(_ci)
        _hor, _vert = _split_byte(fp.read(1))
        horizontal_sampling_factor.append(_hor)
        vertical_sampling_factor.append(_vert)
        _tqi = unpack('>B', fp.read(1))[0]
        quantisation_selector.append(_tqi)

    info = {
        'Lf' : length,
        'P' : precision,
        'Y' : nr_lines,
        'X' : samples_per_line,
        'Nf' : nr_components,
        'Ci' : component_id,
        'Hi' : horizontal_sampling_factor,
        'Vi' : vertical_sampling_factor,
        'Tqi' : quantisation_selector,
    }

    return info


def SOP(fp):
    """Parse a SOP marker segment"""
    lsop = unpack('>H', fp.read(2))[0]
    nsop = unpack('>H', fp.read(2))[0]

    info = {
        'Lsop' : lsop,
        'Nsop' : nsop,
    }

    return info


def SOS(fp, jpg='JPEG'):
    """Read a SOS 'Start of scan' header.

    +-----------+------+----------------------------------------------+
    | Parameter | Size | Values                                       |
    |           |      |---------------------+-------------+----------+
    |           | bits | Sequential          | Progressive | Lossless |
    |           |      +----------+----------+             |          |
    |           |      | Baseline | Extended |             |          |
    +===========+======+==========+==========+=============+==========+
    | Ls        | 16   |  6 + 2 * Ns                                  |
    +-----------+------+----------+----------+-------------+----------+
    | Ns        | 8    | 1 - 4                                        |
    +-----------+------+----------+----------+-------------+----------+
    | Csj       | 8    | 0 - 255                                      |
    +-----------+------+----------+----------+-------------+----------+
    | Tdj       | 4    | 0 - 1    | 0 - 3    | 0 - 3       | 0 - 3    |
    +-----------+------+----------+----------+-------------+----------+
    | Taj       | 4    | 0 - 1    | 0 - 3    | 0 - 3       | 0        |
    +-----------+------+----------+----------+-------------+----------+
    | Ss        | 8    | 0        | 0        | 0 - 63      | 0, 1 - 7 |
    +-----------+------+----------+----------+-------------+----------+
    | Se        | 8    | 63       | 63       | 0, Ss - 63  | 0        |
    +-----------+------+----------+----------+-------------+----------+
    | Ah        | 4    | 0        | 0        | 0 - 13      | 0        |
    +-----------+------+----------+----------+-------------+----------+
    | Al        | 4    | 0        | 0        | 0 - 13      | 0 - 15   |
    +-----------+------+----------+----------+-------------+----------+

    SOS - Start of scan marker
    Ls - Scan header length
    Ns - Number of image components in scan
    Csj - Scan component selector
    Tdj - DC entropy coding table destination selector.
    Taj - AC entropy coding table destination selector. Set to 0 for lossless.
    Ss - Start of spectral or predictor selection. Shall be 0 for sequential
         DCT, for lossless this is the predictor.
    Se - End of spectral selection. Shall be 63 for sequential DCT. In lossless
         this has no meaning and shall be set to 0.
    Ah - Successive approximation bit position high
         In lossless this has no meaning and shall be set to 0.
    Al - Successive approximation bit position low or point transform
         Shall be set to 0 for sequential DCT. In lossless mode specifies
         the point transform Pt.
    """
    (length, nr_components) = unpack('>HB', fp.read(3))

    csj, tdj, taj, tmj = [], [], [], []
    for ii in range(nr_components):
        _cs = unpack('>B', fp.read(1))[0]
        csj.append(_cs)
        if jpg == 'JPEG':
            _td, _ta = _split_byte(fp.read(1))
            tdj.append(_td)
            taj.append(_ta)
        elif jpg == 'JPEG-LS':
            tmj.append(unpack('>B', fp.read(1))[0])


    (ss, se) = unpack('>BB', fp.read(2))
    ah, al = _split_byte(fp.read(1))

    if jpg == 'JPEG':
        return {
            'Ls' : length,
            'Ns' : nr_components,
            'Csj' : csj,
            'Tdj' : tdj,
            'Taj' : taj,
            'Ss' : ss,
            'Se' : se,
            'Ah' : ah,
            'Al' : al,
        }
    elif jpg == 'JPEG-LS':
        return {
            'Ls' : length,
            'Ns' : nr_components,
            'Csj' : csj,
            'Tmj' : tmj,  # 0 to 255
            'NEAR' : ss,  # 0 for lossless, otherwise 1 to min(255, MAXVAL/2)
            'ILV' : se,  # 0 for single component, 1 for interleaved, 2 for sampled interleaved
            'Ah' : ah,
            'Al' : al,
        }


def SOT(fp):
    """Parse an SOT marker segment.

    SOT - Start of tile-part segment
    Lsot - length of marker segment
    Isot - tile index
    Psot - length from the beginning of the first byte of this SOT marker
           segment of the tile-part to the end of the data of that tile-part.
    TPsot - Tile part index
    TNsot - number of tile-parts of a tile in the codestream
    """
    info = {
        'Lsot' : unpack('>H', fp.read(2))[0],
        'Isot' : unpack('>H', fp.read(2))[0],
        'Psot' : unpack('>L', fp.read(4))[0],
        'TPsot' : unpack('B', fp.read(1))[0],
        'TNsot' : unpack('B', fp.read(1))[0]
    }

    return info


def skip(fp):
    length = unpack('>H', fp.read(2))[0]
    fp.seek(length - 2, 1)

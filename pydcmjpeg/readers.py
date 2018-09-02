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
    length = unpack('>H', fp.read(2))[0]
    restart_interval = unpack('>H', fp.read(2))[0]

    info = {
        'Lr' : length,
        'Ri' : restart_interval
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
    _eh, _ev = _split_byte(unpack.read('>B', fp.read(1))[0])

    info = {
        'Le' : length,
        'Eh' : _eh,
        'Ev' : _ev
    }

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


def SOS(fp):
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
    Tdj - DC entropy coding table destination selector
    Taj - AC entropy coding table destination selector
    Ss - Start of spectral or predictor selection
    Se - End of spectral selection
    Ah - Successive approximation bit position high
    Al - Successive approximation bit position low or point transform
    """
    (length, nr_components) = unpack('>HB', fp.read(3))

    csj, tdj, taj = [], [], []
    for ii in range(nr_components):
        _cs = unpack('>B', fp.read(1))[0]
        csj.append(_cs)
        _td, _ta = _split_byte(fp.read(1))
        tdj.append(_td)
        taj.append(_ta)

    (ss, se) = unpack('>BB', fp.read(2))
    ah, al = _split_byte(fp.read(1))

    info = {
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

    return info


def skip(fp):
    length = unpack('>H', fp.read(2))[0]
    fp.seek(length - 2, 1)

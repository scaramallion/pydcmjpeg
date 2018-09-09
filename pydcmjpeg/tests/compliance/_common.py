"""Common data for use in the compliance tests."""

import numpy as np

from pydcmjpeg.config import ZIGZAG
from pydcmjpeg.utils import get_bit


WRITE_SOS_DATA = False
WRITE_SOS_TYPE = 'Sequential DCT'

QUANTIZATION_A = np.asarray(
    [[ 8,  6,  5,  8, 12, 20, 26, 30],
     [ 6,  6,  7, 10, 13, 29, 30, 28],
     [ 7,  7,  8, 12, 20, 29, 35, 28],
     [ 7,  9, 11, 15, 26, 44, 40, 31],
     [ 9, 11, 19, 28, 34, 55, 52, 39],
     [12, 18, 28, 32, 41, 52, 57, 46],
     [25, 32, 39, 44, 52, 61, 60, 51],
     [36, 46, 48, 49, 56, 50, 52, 50]]
)

QUANTIZATION_B = np.asarray(
    [[ 9,  9, 12, 24, 50, 50, 50, 50],
     [ 9, 11, 13, 33, 50, 50, 50, 50],
     [12, 13, 28, 50, 50, 50, 50, 50],
     [24, 33, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50],
     [50, 50, 50, 50, 50, 50, 50, 50]]
)

QUANTIZATION_C = np.asarray(
    [[16, 17, 18, 19, 20, 21, 22, 23],
     [17, 18, 19, 20, 21, 22, 23, 24],
     [18 ,19, 20, 21, 22, 23, 24, 25],
     [19, 20, 21, 22, 23, 24, 25, 26],
     [20, 21, 22, 23, 24, 25, 26, 27],
     [21, 22, 23, 24, 25, 26, 27, 28],
     [22, 23, 24, 25, 26, 27, 28, 29],
     [23, 24, 25, 26, 27, 28, 29, 30]]
)

QUANTIZATION_D = np.asarray(
    [[16, 16, 19, 22, 26, 27, 29, 34],
     [16, 16, 22, 24, 27, 29, 34, 37],
     [19, 22, 26, 27, 29, 34, 34, 38],
     [22, 22, 26, 27, 29, 34, 37, 40],
     [22, 26, 27, 29, 32, 35, 40, 48],
     [26, 27, 29, 32, 25, 40, 48, 58],
     [26, 27, 29, 34, 38, 46, 56, 69],
     [27, 29, 35, 38, 46, 56, 69, 83]]
)


def _write_soi(fp, offset, marker, name, info):
    fp.write('{0:<7}{1:<4}({2})\n'.format(offset, name, marker))

def _write_com(fp, offset, marker, name, info):
    comment = "'" + info['Cm'].decode('utf-8') + "'"
    # First line has 46 characters, the remaining is 63 characters/line
    fp.write(
        "{0:<7}{1:<4}({2}) Lc={3} {4}\n"
        .format(offset, name, marker, info['Lc'], comment[:47])
    )
    comment = comment[47:]

    while True:
        if not comment:
            break
        line = comment[:63]
        comment = comment[63:]

        fp.write("         {}\n".format(line))

def _write_dqt(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lq={3}\n"
        .format(offset, name, marker, info['Lq'])
    )
    for pq, tq, qk in zip(info['Pq'], info['Tq'], info['Qk']):
        _prec = '2' if pq else '1'
        if pq:
            fp.write(
                'Qtable {0},  Precision = {1} bytes.  Source must be > 8 bits.\n'
                .format(tq, _prec)
            )
        else:
            fp.write(
                'Qtable {0},  Precision = {1} byte.\n'.format(tq, _prec)
            )

        new_qk = []
        for index in ZIGZAG:
            new_qk.append(qk[index])

        for ii in range(0, 64, 8):
            if not pq:
                _line = '   '.join(['{:>2}'.format(qq) for qq in new_qk[ii:ii + 8]])
            else:
                _line = '    '.join(['{:>3}'.format(qq) for qq in new_qk[ii:ii + 8]])
            fp.write('             {}\n'.format(_line))

def _write_dri(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lr={3} Ri={4}\n"
        .format(offset, name, marker, info['Lr'], info['Ri'])
    )

def _write_sof(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lf={3} P={4} Y={5} X={6} Nf={7}"
        .format(offset, name, marker, info['Lf'], info['P'], info['Y'],
        info['X'], info['Nf'])
    )

    if name == 'SOF0':
        fp.write('  (baseline seq. DCT)\n')
    elif name == 'SOF1':
        fp.write('  (ext. seq. DCT/Huff.)\n')
    elif name == 'SOF3':
        fp.write('  (seq. lossless/Huff)\n')
    else:
        raise NotImplementedError

    for ci, h, v, tqi in zip(info['Ci'], info['Hi'], info['Vi'], info['Tqi']):
        fp.write(
            '             Ci={0:>3} HV={1}{2} Tqi={3}\n'
            .format(ci, h, v, tqi)
        )

def _write_dht(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Lq={3}\n"
        .format(offset, name, marker, info['Lh'])
    )
    for tc, th, li, vij in zip(info['Tc'], info['Th'], info['Li'], info['Vij']):
        if tc == 0:
            fp.write('Lossless/DC Huffman table {}\n'.format(th))
        elif tc == 1:
            fp.write('AC Huffman table {}\n'.format(th))
        else:
            raise NotImplementedError

        fp.write(':(  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16   code lengths       )\n')
        nr_values = ' '.join(['{:>02x}'.format(val) for val in li])
        fp.write('   {} :(values/length (hex))\n'.format(nr_values))

        for ii, values in enumerate(vij):
            if values is not None:
                for jj in range(0, len(values), 16):
                    val = ' '.join(['{:>02x}'.format(vv) for vv in values[jj:jj+16]])
                    fp.write('   {:<47}'.format(val))
                    fp.write(' :(hex values, L={:>2})\n'.format(ii + 1))

def _write_app(fp, offset, marker, name, info):
    app = info['Ap'].decode('utf-8')
    app_info = "'" + app + "'"
    # First line has 46 characters, the remaining is 63 characters/line
    fp.write(
        "{0:<7}{1:<4}({2}) Lp={3} {4}\n"
        .format(offset, name, marker, info['Lp'], app_info[:47])
    )

    for ii in range(46, len(app_info), 63):
        fp.write("         {}\n".format(app_info[ii:ii + 63]))

def _write_sos(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2}) Ls={3} Ns={4}\n"
        .format(offset, name, marker, info['Ls'], info['Ns'])
    )

    for csk, td, ta in zip(info['Csj'], info['Tdj'], info['Taj']):
        fp.write(
            '             Csk={0:>3} Td={1} Ta={2}\n'
            .format(csk, td, ta)
        )

    if WRITE_SOS_TYPE == 'Sequential DCT':
        fp.write(
            '             Ss={} Se={} Ah={} Al={}\n'
            .format(info['Ss'], info['Se'], info['Ah'], info['Al'])
        )
    elif WRITE_SOS_TYPE == 'Lossless':
        fp.write(
            '             P sel={} Pt={}\n'.format(info['Ss'], info['Al'])
        )

    if not WRITE_SOS_DATA:
        return

    # Write RST and encoded data lengths
    remove = ['Ls', 'Ns', 'Csj', 'Tdj', 'Taj', 'Ss', 'Se', 'Ah', 'Al']
    keys = [kk for kk in info if kk not in remove]
    keys = sorted(keys, key=lambda x: int(x.split('@')[1]))
    for key in keys:
        if key.split('@')[0] == 'ENC':
            fp.write(
                '       {} bytes of entropy-coded data\n'
                .format(len(info[key]))
            )
        else:
            (name, offset) = key.split('@')
            fp.write(
                '{:<7}{}({})\n'.format(offset, name, 'ffd{}'.format(name[-1]))
            )

def _write_eoi(fp, offset, marker, name, info):
    fp.write(
        "{0:<7}{1:<4}({2})\n"
        .format(offset, name, marker)
    )

def _write_soc(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )
    fp.write('\n')

def _write_siz(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )
    fp.write('\n')

    fp.write('  {:<31}: JPEG2000 profile {}\n'.format('Required Capabilities', info['Rsiz'] - 1))
    fp.write('  {:<31}: {}x{}\n'.format('Reference Grid Size', info['Xsiz'], info['Ysiz']))
    fp.write('  {:<31}: {}x{}\n'.format('Image Offset', info['XOsiz'], info['YOsiz']))
    fp.write('  {:<31}: {}x{}\n'.format('Reference Tile Size', info['XTsiz'], info['YTsiz']))
    fp.write('  {:<31}: {}x{}\n'.format('Reference Tile Offset', info['XTOsiz'], info['YTOsiz']))
    fp.write('  {:<31}: {}\n'.format('Components', info['Csiz']))
    for ii in range(info['Csiz']):
        ssiz = info['Ssiz'][ii]
        if ssiz & (1 << 7):
            # Signed
            is_signed = 'yes'
            bit_depth = (ssiz & b'\x7f'[0]) + 1
        else:
            # Unsigned
            is_signed = 'no'
            bit_depth = ssiz + 1

        sep = '{}x{}'.format(info['XRsiz'][ii], info['YRsiz'][ii])

        depth_str = 'Component #{} Depth'.format(ii)
        signed_str = 'Component #{} Signed'.format(ii)
        sep_str = 'Component #{} Sample Separation'.format(ii)
        fp.write('  {:<31}: {}\n'.format(depth_str, bit_depth))
        fp.write('  {:<31}: {}\n'.format(signed_str, is_signed))
        fp.write('  {:<31}: {}\n'.format(sep_str, sep))

    fp.write('\n')

def _write_qcd(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )
    fp.write('\n')

    # Sqcd xxx0 0000 is not quant
    # 000x xxxx to 111 x xxxx is nr guard bits
    sqcd = info['Sqcd']
    split_3 = (sqcd & 224) >> 5
    split_5 = (sqcd & 31)
    if split_5 == 0:
        qcd_str = 'none'
    elif split_5 == 1:
        qcd_str = 'scalar derived'
    elif split_5 == 2:
        qcd_str = 'scalar expounded'

    fp.write('  {:<18}: {}\n'.format('Quantization Type', qcd_str))
    fp.write('  {:<18}: {}\n'.format('Guard Bits', split_3))

    if split_5 == 0:
        for ii, value in enumerate(info['SPqcd']):
            value = (value & 248) >> 3
            fp.write('  {:<18}: {}\n'.format('Exponent #{}'.format(ii), value))
    else:
        mantissa = (value & 4097)
        exponent = (value & 63488) >> 11
        fp.write('  {:<18}: {}\n'.format('Mantissa #{}'.format(ii), mantissa))
        fp.write('  {:<18}: {}\n'.format('Exponent #{}'.format(ii), exponent))

    fp.write('\n')

def _write_cod(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )

    fp.write('\n')

    scod = info['Scod']
    sgcod = info['SGcod']
    spcod = info['SPcod']

    default_precincts = 'yes'
    if get_bit(scod, 7):
        default_precincts = 'no'

    sop_markers = 'no'
    if get_bit(scod, 6):
        sop_markers = 'yes'

    eph_markers = 'no'
    if get_bit(scod, 5):
        eph_markers = 'yes'

    prog_order = {
        0 : 'layer-resolution level-component-position',
        1 : 'resolution level-layer-component-position',
        2 : 'resolution level-position-component-layer',
        3 : 'position-component-resolution level-layer',
        4 : 'component-position-resolution level-layer',
    }

    mc_transform = 'none'
    if sgcod['mc_transform'] == 1:
        mc_transform = 'Component transformation'

    selective_arith = 'no'
    block_style = spcod['block_style']
    if get_bit(block_style, 7):
        selective_arith = 'yes'

    context_reset = 'no'
    if get_bit(block_style, 6):
        context_reset = 'yes'

    termination = 'no'
    if get_bit(block_style, 5):
        termination = 'yes'

    vertically = 'no'
    if get_bit(block_style, 4):
        vertically = 'yes'

    predictable = 'no'
    if get_bit(block_style, 3):
        predictable = 'yes'

    segmentation = 'no'
    if get_bit(block_style, 2):
        segmentation = 'yes'

    wavelet = '9-7 irreversible'
    if spcod['transform']:
        wavelet = '5-3 reversible'

    fp.write('  {:<35}: {}\n'.format('Default Precincts of 2^15x2^15', default_precincts))
    fp.write('  {:<35}: {}\n'.format('SOP Marker Segments', sop_markers))
    fp.write('  {:<35}: {}\n'.format('EPH Marker Segments', eph_markers))

    # FIXME
    fp.write('  {:<35}: {:08}\n'.format('All Flags', scod))

    fp.write('  {:<35}: {}\n'.format('Progression Order', prog_order[sgcod['progression_order']]))
    fp.write('  {:<35}: {}\n'.format('Layers', sgcod['nr_layers']))
    fp.write('  {:<35}: {}\n'.format('Multiple Component Transformation', mc_transform))
    fp.write('  {:<35}: {}\n'.format('Decomposition Levels', spcod['decomp_levels']))

    width = spcod['block_width']
    width = 2**((width & 0b00001111) + 2)
    height = spcod['block_height']
    height = 2**((height & 0b00001111) + 2)

    fp.write('  {:<35}: {}x{}\n'.format('Code-block size', width, height))
    fp.write('  {:<35}: {}\n'.format('Selective Arithmetic Coding Bypass', selective_arith))
    fp.write('  {:<35}: {}\n'.format('Reset Context Probabilities', context_reset))
    fp.write('  {:<35}: {}\n'.format('Termination on Each Coding Pass', termination))
    fp.write('  {:<35}: {}\n'.format('Vertically Causal Context', vertically))
    fp.write('  {:<35}: {}\n'.format('Predictable Termination', predictable))
    fp.write('  {:<35}: {}\n'.format('Segmentation Symbols', segmentation))
    fp.write('  {:<35}: {}\n'.format('Wavelet Transformation', wavelet))

    fp.write('\n')

def _write_sot(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )
    fp.write('\n')

    fp.write('  {:<12}: {}\n'.format('Tile', info['Isot']))
    fp.write('  {:<12}: {}\n'.format('Length', info['Psot']))
    fp.write('  {:<12}: {}\n'.format('Index', info['TPsot']))
    fp.write('  {:<12}: {}\n'.format('Tile-Parts:', info['TNsot']))

    fp.write('\n')

def _write_sod(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )

    fp.write('\n')

    #fp.write('Data : {} bytes\n'.format('FIXME'))

    #fp.write('\n')

def _write_eoc(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<7}{1:<4}({2})\n"
        .format(offset, name, marker)
    )

    fp.write('\n')

def _write_coc(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )

    fp.write('\n')

    ccoc = info['Ccoc']

    fp.write('  {:<35}: {}\n'.format('Component', ccoc))

    scoc = info['Scoc']

    has_precincts = get_bit(scoc, 7)
    precincts = 'default'
    if has_precincts:
        raise NotImplementedError

    fp.write('  {:<35}: {}\n'.format('Precincts', precincts))

    spcoc = info['SPcoc']

    selective_arith = 'no'
    block_style = spcoc['block_style']
    if get_bit(block_style, 7):
        selective_arith = 'yes'

    context_reset = 'no'
    if get_bit(block_style, 6):
        context_reset = 'yes'

    termination = 'no'
    if get_bit(block_style, 5):
        termination = 'yes'

    vertically = 'no'
    if get_bit(block_style, 4):
        vertically = 'yes'

    predictable = 'no'
    if get_bit(block_style, 3):
        predictable = 'yes'

    segmentation = 'no'
    if get_bit(block_style, 2):
        segmentation = 'yes'

    wavelet = '9-7 irreversible'
    if spcoc['transform']:
        wavelet = '5-3 reversible'

    fp.write('  {:<35}: {}\n'.format('Decomposition Levels', spcoc['decomp_levels']))

    width = spcoc['block_width']
    width = 2**((width & 0b00001111) + 2)
    height = spcoc['block_height']
    height = 2**((height & 0b00001111) + 2)

    fp.write('  {:<35}: {}x{}\n'.format('Code-block size', width, height))
    fp.write('  {:<35}: {}\n'.format('Selective Arithmetic Coding Bypass', selective_arith))
    fp.write('  {:<35}: {}\n'.format('Reset Context Probabilities', context_reset))
    fp.write('  {:<35}: {}\n'.format('Termination on Each Coding Pass', termination))
    fp.write('  {:<35}: {}\n'.format('Vertically Causal Context', vertically))
    fp.write('  {:<35}: {}\n'.format('Predictable Termination', predictable))
    fp.write('  {:<35}: {}\n'.format('Segmentation Symbols', segmentation))
    fp.write('  {:<35}: {}\n'.format('Wavelet Transformation', wavelet))

    fp.write('\n')

def _write_com_jp2(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )

    fp.write('\n')

    if info['Rcom'] == 0:
        registration = 'binary'
    elif info['Rcom'] == 1:
        registration = 'ISO-8859-15'

    fp.write('  {:<13}: {}\n'.format('Registration', registration))
    fp.write('  {:<13}: {}\n'.format('Comment', info['Ccom'].decode('iso8859-15')))

    fp.write('\n')

def _write_res(fp, offset, marker, name, description, info):
    name = '0x30'
    description = 'unknown segment-less'
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )

    fp.write('\n')

def _write_sop(fp, offset, marker, name, description, info):
    fp.write(
        "{0:<8}: New marker: {1} ({2})\n"
        .format(offset, name, description)
    )

    fp.write('\n')

    fp.write('  Sequence : {}\n'.format(info['Nsop']))

    fp.write('\n')


WRITERS = {
    'SOI' : _write_soi,
    'COM' : _write_com,
    'DQT' : _write_dqt,
    'DRI' : _write_dri,
    'SOF' : _write_sof,
    'DHT' : _write_dht,
    'APP' : _write_app,
    'SOS' : _write_sos,
    'EOI' : _write_eoi,
    'EOC' : _write_eoc,
    'SIZ' : _write_siz,
    'SOC' : _write_soc,
    'QCD' : _write_qcd,
    'COD' : _write_cod,
    'SOT' : _write_sot,
    'SOD' : _write_sod,
    'COC' : _write_coc,
    'COM_JP2' : _write_com_jp2,
    'RES' : _write_res,
    'SOP' : _write_sop,
}

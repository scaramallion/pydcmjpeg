"""Decoders for 10918-1 Baseline DCT JPEGs."""

from pydcmjpeg.config import ZIGZAG
from pydcmjpeg.huffman import _get_huffman


# Temporary to aid in debugging
def _debug_sos(offset, marker, name, info):
    print(
        "{0:<7}{1:<4}({2}) Ls={3} Ns={4}"
        .format(offset, name, marker, info['Ls'], info['Ns'])
    )

    for csk, td, ta in zip(info['Csj'], info['Tdj'], info['Taj']):
        print(
            '             Csk={0:>3} Td={1} Ta={2}'
            .format(csk, td, ta)
        )

    print(
        '             Ss={} Se={} Ah={} Al={}'
        .format(info['Ss'], info['Se'], info['Ah'], info['Al'])
    )

    # Write RST and encoded data lengths
    remove = ['Ls', 'Ns', 'Csj', 'Tdj', 'Taj', 'Ss', 'Se', 'Ah', 'Al']
    keys = [kk for kk in info if kk not in remove]
    keys = sorted(keys, key=lambda x: int(x.split('@')[1]))
    for key in keys:
        if key.split('@')[0] == 'ENC':
            print(
                '       {} bytes of entropy-coded data'
                .format(len(info[key]))
            )
        else:
            (name, offset) = key.split('@')
            print(
                '{:<7}{}({})'.format(offset, name, 'ffd{}'.format(name[-1]))
            )

def _debug_dht(offset, marker, name, info):
    print(
        "{0:<7}{1:<4}({2}) Lq={3}"
        .format(offset, name, marker, info['Lh'])
    )
    for tc, th, li, vij in zip(info['Tc'], info['Th'], info['Li'], info['Vij']):
        if tc == 0:
            print('Lossless/DC Huffman table {}'.format(th))
        elif tc == 1:
            print('AC Huffman table {}'.format(th))
        else:
            raise NotImplementedError

        print(':(  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16   code lengths       )\n')
        nr_values = ' '.join(['{:>02x}'.format(val) for val in li])
        print('   {} :(values/length (hex))'.format(nr_values))

        for ii, values in enumerate(vij):
            if values is not None:
                for jj in range(0, len(values), 16):
                    val = ' '.join(['{:>02x}'.format(vv) for vv in values[jj:jj+16]])
                    print(
                        '   {:<47} :(hex values, L={:>2})'
                        .format(val, ii + 1)
                    )

def _debug_dqt(offset, marker, name, info):
    print(
        "{0:<7}{1:<4}({2}) Lq={3}"
        .format(offset, name, marker, info['Lq'])
    )
    for pq, tq, qk in zip(info['Pq'], info['Tq'], info['Qk']):
        _prec = '2' if pq else '1'
        if pq:
            print(
                'Qtable {0},  Precision = {1} bytes.  Source must be > 8 bits.'
                .format(tq, _prec)
            )
        else:
            print(
                'Qtable {0},  Precision = {1} byte.'.format(tq, _prec)
            )

        new_qk = []
        for index in ZIGZAG:
            new_qk.append(qk[index])

        for ii in range(0, 64, 8):
            if not pq:
                _line = '   '.join(['{:>2}'.format(qq) for qq in new_qk[ii:ii + 8]])
            else:
                _line = '    '.join(['{:>3}'.format(qq) for qq in new_qk[ii:ii + 8]])
            print('             {}'.format(_line))


def decode_baseline(jpg):
    """

    """

    # For each SOS in the file
    #   For each component, j, in the scan
    #       Determine the quantization table, Cs(j)
    #       Determine the DC table, Td(j)
    #       Determine the AC table, Ta(j)

    # Quantisation tables
    q_tables = {}
    for key in jpg.get_keys('DQT'):
        (marker, fill_bytes, dqt) = jpg.info[key]
        #_debug_dqt(key.split('@')[1], marker, 'DQT', dqt)
        for table_id, quantisation_table in zip(dqt['Tq'], dqt['Qk']):
            q_tables[table_id] = quantisation_table

    # Huffman tables: up to 2 AC and 2 DC
    h_tables = {
        0 : {},  # DC or lossless
        1 : {}  # AC
    }
    for key in jpg.get_keys('DHT'):
        (marker, fill_bytes, dht) = jpg.info[key]
        _debug_dht(key.split('@')[1], marker, 'DHT', dht)
        for _id, _type, bits, huffval in zip(dht['Tc'], dht['Th'], dht['Li'], dht['Vij']):
            h_tables[_type][_id] = (bits, huffval)

    huff_tables = _get_huffman(h_tables)

    sos_keys = jpg.get_keys('SOS')
    if not sos_keys:
        raise ValueError(
            "Unable to decode the JPEG file as it contains no 'SOS' markers"
        )

    for key in sos_keys:
        print("Decoding scan: '{}'".format(key))
        (marker, fill_bytes, scan) = jpg.info[key]

        # Debugging output
        _debug_sos(key.split('@')[1], marker, 'SOS', scan)

        csk, td, ta = scan['Csk'], scan['Td'], scan['Ta']

        # For the encoded data in the scan
        enc_keys = [kk for kk in scan.keys() if 'ENC' in kk]
        enc_keys = sorted(enc_keys, key=lambda x: int(x.split('@')[1]))

        # The encoded data still contains 0xFF 0x00 bytes
        for enc_key in enc_keys:
            print("Decoded encoded data: '{}'".format(enc_key))
            encoded_data = scan[enc_key]
            print(encoded_data)
            for bb in encoded_data:
                print('{:>08b}'.format(bb))

            for cs, dc_id, ac_id in zip(csk, td, ta):
                dc_huff = h_tables[0][dc_id]
                ac_huff = h_tables[1][ac_id]

                pass

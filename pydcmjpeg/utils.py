

def split_byte(bs):
    """Split the 8-bit byte `bs` into two 4-bit integers."""
    mask_msb = 0b11110000
    mask_lsb = 0b00001111

    return (mask_msb & bs[0]) >> 4, mask_lsb & bs[0]


def get_bit(byte, ii):
    """Return the bit value at index `ii` of `byte`.

    Bit index is 0 = MSB, 7 = LSB
    """
    return (byte >> (7 - ii)) & 1

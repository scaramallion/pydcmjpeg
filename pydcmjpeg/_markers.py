from pydcmjpeg.readers import *


MARKERS = {}
# JPEG reserved markers
for _marker in range(0xFF02, 0xFFBF + 1):
    MARKERS[_marker] = ('RES', 'Reserved', None)

MARKERS.update({
    0xFF01 : ('TEM', 'For temporary private use in artithmetic coding', None),  # Standalone
    0xFF4F : ('SOC', 'Start of codestream', None),  # JPEG 2000 *
    0xFF51 : ('SIZ', 'Image and tile size', SIZ),  # JPEG 2000
    0xFF52 : ('COD', 'Coding style default', COD),  # JPEG 2000
    0xFF53 : ('COC', 'Coding style component', COC),  # JPEG 2000
    0xFF55 : ('TLM', 'Tile-part lengths', None),  # JPEG 2000
    0xFF57 : ('PLM', 'Packet length, main header', None),  # JPEG 2000
    0xFF58 : ('PLT', 'Packet length, tile-part header', None),  # JPEG 2000
    0xFF5C : ('QCD', 'Quantization default', QCD),  # JPEG 2000
    0xFF5D : ('QCC', 'Quantization component', None),  # JPEG 2000
    0xFF5E : ('RGN', 'Region of interest', None),  # JPEG 2000
    0xFF5F : ('POC', 'Progression order change', None),  # JPEG 2000
    0xFF60 : ('PPM', 'Packed packet headers, main header', None),  # JPEG 2000
    0xFF61 : ('PPT', 'Packed packet headers ,tile-part header', None),  # JPEG 2000
    0xFF63 : ('CRG', 'Component registration', None),  # JPEG 2000
    0xFF64 : ('COM', 'Comment', COM_JP2),  # JPEG 2000
    0xFF90 : ('SOT', 'Start of tile-part', SOT),  # JPEG 2000 *
    0xFF91 : ('SOP', 'Start of packet', SOP),  # JPEG 2000
    0xFF92 : ('EPH', 'End of packet header', None),  # JPEG 2000
    0xFF93 : ('SOD', 'Start of data', SOD),  # JPEG 2000 *
    # Start of frame markers, non-differential, Huffman coding
    0xFFC0 : ('SOF0', 'Baseline DCT', SOF),
    0xFFC1 : ('SOF1', 'Extended sequential DCT', SOF),
    0xFFC2 : ('SOF2', 'Progressive DCT', SOF),
    0xFFC3 : ('SOF3', 'Lossless (sequential)', SOF),
    # Huffman table specification
    0xFFC4 : ('DHT', 'Define Huffman table(s)', DHT),
    # Start of frame markers, differential, Huffman coding
    0xFFC5 : ('SOF5', 'Differential sequential DCT', SOF),
    0xFFC6 : ('SOF6', 'Differential progressive DCT', SOF),
    0xFFC7 : ('SOF7', 'Differential lossless (sequential)', SOF),
    # Start of frame markers, non-differential, arithmetic coding
    0xFFC8 : ('JPG', 'Reserved for JPEG extensions', None),
    0xFFC9 : ('SOF9', 'Extended sequential DCT', SOF),
    0xFFCA : ('SOF10', 'Progressive DCT', SOF),
    0xFFCB : ('SOF11', 'Lossless (sequential)', SOF),
    # Define arithmetic coding conditioning(s)
    0xFFCC : ('DAC', 'Define arithmetic coding conditioning(s)', DAC),
    # Start of frame markers, differential, arithmetic coding
    0xFFCD : ('SOF13', 'Differential sequential DCT', SOF),
    0xFFCE : ('SOF14', 'Differential progressive DCT', SOF),
    0xFFCF : ('SOF15', 'Differential lossless (sequential)', SOF),
    # Restart interval termination
    0xFFD0 : ('RST0', 'Restart with modulo 8, count "0"', None),  # Standalone
    0xFFD1 : ('RST1', 'Restart with modulo 8, count "1"', None),  # Standalone
    0xFFD2 : ('RST2', 'Restart with modulo 8, count "2"', None),  # Standalone
    0xFFD3 : ('RST3', 'Restart with modulo 8, count "3"', None),  # Standalone
    0xFFD4 : ('RST4', 'Restart with modulo 8, count "4"', None),  # Standalone
    0xFFD5 : ('RST5', 'Restart with modulo 8, count "5"', None),  # Standalone
    0xFFD6 : ('RST6', 'Restart with modulo 8, count "6"', None),  # Standalone
    0xFFD7 : ('RST7', 'Restart with modulo 8, count "7"', None),  # Standalone
    # Other markers
    0xFFD8 : ('SOI', 'Start of image', None),  # Standalone
    0xFFD9 : ('EOI', 'End of image', None),  # Standalone, EOC in JPEG2K
    0xFFDA : ('SOS', 'Start of scan', SOS),
    0xFFDB : ('DQT', 'Define quantization', DQT),
    0xFFDC : ('DNL', 'Define number of lines', DNL),
    0xFFDD : ('DRI', 'Define restart interval', DRI),
    0xFFDE : ('DHP', 'Define hierarchical progression', SOF),
    0xFFDF : ('EXP', 'Expand reference component(s)', EXP),
    0xFFE0 : ('APP0', 'Reserved for application segments', APP),
    0xFFE1 : ('APP1', 'Reserved for application segments', APP),
    0xFFE2 : ('APP2', 'Reserved for application segments', APP),
    0xFFE3 : ('APP3', 'Reserved for application segments', APP),
    0xFFE4 : ('APP4', 'Reserved for application segments', APP),
    0xFFE5 : ('APP5', 'Reserved for application segments', APP),
    0xFFE6 : ('APP6', 'Reserved for application segments', APP),
    0xFFE7 : ('APP7', 'Reserved for application segments', APP),
    0xFFE8 : ('APP8', 'Reserved for application segments', APP),
    0xFFE9 : ('APP9', 'Reserved for application segments', APP),
    0xFFEA : ('APP10', 'Reserved for application segments', APP),
    0xFFEB : ('APP11', 'Reserved for application segments', APP),
    0xFFEC : ('APP12', 'Reserved for application segments', APP),
    0xFFED : ('APP13', 'Reserved for application segments', APP),
    0xFFEE : ('APP14', 'Reserved for application segments', APP),
    0xFFEF : ('APP15', 'Reserved for application segments', APP),
    0xFFF0 : ('JPG0', 'Reserved for JPEG extensions', None),  # 10918-3
    0xFFF1 : ('JPG1', 'Reserved for JPEG extensions', None),  # 10918-3
    0xFFF2 : ('JPG2', 'Reserved for JPEG extensions', None),  # 10918-3
    0xFFF3 : ('JPG3', 'Reserved for JPEG extensions', None),  # 10918-3
    0xFFF4 : ('JPG4', 'Reserved for JPEG extensions', None),  # 10918-3
    0xFFF5 : ('JPG5', 'Reserved for JPEG extensions', None),  # 10918-3
    0xFFF6 : ('JPG6', 'Reserved for JPEG extensions', None),  # 10918-3
    0xFFF7 : ('SOF55', 'Start of frame (JPEG-LS)', SOF),  # 14495-1
    0xFFF8 : ('LSE', 'Beginning of preset parameters (JPEG-LS)', LSE),  # 14495-1
    0xFFF9 : ('JPG9', 'Reserved for JPEG extensions', None),
    0xFFFA : ('JPG10', 'Reserved for JPEG extensions', None),
    0xFFFB : ('JPG11', 'Reserved for JPEG extensions', None),
    0xFFFC : ('JPG12', 'Reserved for JPEG extensions', None),
    0xFFFD : ('JPG13', 'Reserved for JPEG extensions', None),
    0xFFFE : ('COM', 'Comment', COM),
})

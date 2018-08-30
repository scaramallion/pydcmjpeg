from pyjpeg.readers import *

MARKERS = {
    # Reserved markers
    0xFF01 : ('TEM', 'For temporary private use in artithmetic coding', None),  # Standalone
    0xFF02 : ('RES', 'Reserved'),
    # Start of frame markers, non-differential, Huffman coding
    0xFFC0 : ('SOF_00', 'Baseline DCT', SOF),
    0xFFC1 : ('SOF_01', 'Extended sequential DCT', SOF),
    0xFFC2 : ('SOF_02', 'Progressive DCT', SOF),
    0xFFC3 : ('SOF_03', 'Lossless (sequential)', SOF),
    # Huffman table specification
    0xFFC4 : ('DHT', 'Define Huffman table(s)', DHT),
    # Start of frame markers, differential, Huffman coding
    0xFFC5 : ('SOF_05', 'Differential sequential DCT', SOF),
    0xFFC6 : ('SOF_06', 'Differential progressive DCT', SOF),
    0xFFC7 : ('SOF_07', 'Differential lossless (sequential)', SOF),
    # Start of frame markers, non-differential, arithmetic coding
    0xFFC8 : ('JPG', 'Reserved for JPEG extensions', None),
    0xFFC9 : ('SOF_09', 'Extended sequential DCT', SOF),
    0xFFCA : ('SOF_10', 'Progressive DCT', SOF),
    0xFFCB : ('SOF_11', 'Lossless (sequential)', SOF),
    # Define arithmetic coding conditioning(s)
    0xFFCC : ('DAC', 'Define arithmetic coding conditioning(s)', skip),
    # Start of frame markers, differential, arithmetic coding
    0xFFCD : ('SOF_13', 'Differential sequential DCT', SOF),
    0xFFCE : ('SOF_14', 'Differential progressive DCT', SOF),
    0xFFCF : ('SOF_15', 'Differential lossless (sequential)', SOF),
    # Restart interval termination
    0xFFD0 : ('RST_0', 'Restart with modulo 8, count "0"', None),  # Standalone
    0xFFD1 : ('RST_1', 'Restart with modulo 8, count "1"', None),  # Standalone
    0xFFD2 : ('RST_2', 'Restart with modulo 8, count "2"', None),  # Standalone
    0xFFD3 : ('RST_3', 'Restart with modulo 8, count "3"', None),  # Standalone
    0xFFD4 : ('RST_4', 'Restart with modulo 8, count "4"', None),  # Standalone
    0xFFD5 : ('RST_5', 'Restart with modulo 8, count "5"', None),  # Standalone
    0xFFD6 : ('RST_6', 'Restart with modulo 8, count "6"', None),  # Standalone
    0xFFD7 : ('RST_7', 'Restart with modulo 8, count "7"', None),  # Standalone
    # Other markers
    0xFFD8 : ('SOI', 'Start of image', SOI),  # Standalone
    0xFFD9 : ('EOI', 'End of image', None),  # Standalone
    0xFFDA : ('SOS', 'Start of scan', SOS),
    0xFFDB : ('DQT', 'Define quantization', DQT),
    0xFFDC : ('DNL', 'Define number of lines', skip),
    0xFFDD : ('DRI', 'Define restart interval', DRI),
    0xFFDE : ('DHP', 'Define hierarchical progression', skip),
    0xFFDF : ('EXP', 'Expand reference component(s)', skip),
    0xFFE0 : ('APP_0', 'Reserved for application segments', APP),
    0xFFE1 : ('APP_1', 'Reserved for application segments', APP),
    0xFFE2 : ('APP_2', 'Reserved for application segments', APP),
    0xFFE3 : ('APP_3', 'Reserved for application segments', APP),
    0xFFE4 : ('APP_4', 'Reserved for application segments', APP),
    0xFFE5 : ('APP_5', 'Reserved for application segments', APP),
    0xFFE6 : ('APP_6', 'Reserved for application segments', APP),
    0xFFE7 : ('APP_7', 'Reserved for application segments', APP),
    0xFFE8 : ('APP_8', 'Reserved for application segments', APP),
    0xFFE9 : ('APP_9', 'Reserved for application segments', APP),
    0xFFEA : ('APP_10', 'Reserved for application segments', APP),
    0xFFEB : ('APP_11', 'Reserved for application segments', APP),
    0xFFEC : ('APP_12', 'Reserved for application segments', APP),
    0xFFED : ('APP_13', 'Reserved for application segments', APP),
    0xFFEE : ('APP_14', 'Reserved for application segments', APP),
    0xFFEF : ('APP_15', 'Reserved for application segments', APP),
    0xFFF0 : ('JPG_0', 'Reserved for JPEG extensions', None),
    0xFFF1 : ('JPG_1', 'Reserved for JPEG extensions', None),
    0xFFF2 : ('JPG_2', 'Reserved for JPEG extensions', None),
    0xFFF3 : ('JPG_3', 'Reserved for JPEG extensions', None),
    0xFFF4 : ('JPG_4', 'Reserved for JPEG extensions', None),
    0xFFF5 : ('JPG_5', 'Reserved for JPEG extensions', None),
    0xFFF6 : ('JPG_6', 'Reserved for JPEG extensions', None),
    0xFFF7 : ('JPG_7', 'Reserved for JPEG extensions', None),
    0xFFF8 : ('JPG_8', 'Reserved for JPEG extensions', None),
    0xFFF9 : ('JPG_9', 'Reserved for JPEG extensions', None),
    0xFFFA : ('JPG_10', 'Reserved for JPEG extensions', None),
    0xFFFB : ('JPG_11', 'Reserved for JPEG extensions', None),
    0xFFFC : ('JPG_12', 'Reserved for JPEG extensions', None),
    0xFFFD : ('JPG_13', 'Reserved for JPEG extensions', None),
    0xFFFE : ('COM', 'Comment', COM),
}

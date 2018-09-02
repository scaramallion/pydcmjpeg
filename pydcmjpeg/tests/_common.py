
import os

COMPL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../', 'data', 'compliance')
)

CPROCESS01 = os.path.join(COMPL_DIR, '10918', 'process_01')
CPROCESS02 = os.path.join(COMPL_DIR, '10918', 'process_02')
CPROCESS04 = os.path.join(COMPL_DIR, '10918', 'process_04')
CPROCESS14 = os.path.join(COMPL_DIR, '10918', 'process_14')

DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../', 'data', 'images')
)

DPROCESS01 = os.path.join(DATA_DIR, '10918', 'process_01')
DPROCESS02 = os.path.join(DATA_DIR, '10918', 'process_02')
DPROCESS04 = os.path.join(DATA_DIR, '10918', 'process_04')
DPROCESS14 = os.path.join(DATA_DIR, '10918', 'process_14')
DPROCESS14SV1 = os.path.join(DATA_DIR, '10918', 'process_14_sv1')

REFERENCE_DATA = {
    'p1' : [
        (os.path.join(CPROCESS01, 'A1.JPG'), None),
        (os.path.join(CPROCESS01, 'B2.JPG'), None),
        (os.path.join(DPROCESS01, '001.jpg'), None),
        (os.path.join(DPROCESS01, 'color3d_jpeg_baseline_422_frame1.jpg'), None),
        (os.path.join(DPROCESS01, 'grey_8.jpg'), None),
        (os.path.join(DPROCESS01, 'huff_simple0.jpg'), None),
        (os.path.join(DPROCESS01, 'rgb_8_422.jpg'), None),
        (os.path.join(DPROCESS01, 'rgb_8_444.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_dcmtk_+eb+cr.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_dcmtk_+eb+cy+n1.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_dcmtk_+eb+cy+n2.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_dcmtk_+eb+cy+np.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_dcmtk_+eb+cy+s4.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_jpeg_dcmtk.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_jpeg_lossy_gdcm.jpg'), None),
        (os.path.join(DPROCESS01, 'SC_rgb_small_odd_jpeg.jpg'), None),
    ],
    'p2' : [
        (os.path.join(CPROCESS02, 'C1.JPG'), None),
        (os.path.join(CPROCESS02, 'C2.JPG'), None),
        (os.path.join(DPROCESS02, 'grey_8.jpg'), None),
        (os.path.join(DPROCESS02, 'rgb_8_422.jpg'), None),
        (os.path.join(DPROCESS02, 'rgb_8_444.jpg'), None),
    ],
    'p3' : None,
    'p4' : [
        (os.path.join(DPROCESS04, 'JPEG-lossy.jpg'), None),
        (os.path.join(DPROCESS04, 'grey_12.jpg'), None),
        (os.path.join(DPROCESS04, 'rgb_12_422.jpg'), None),
        (os.path.join(DPROCESS04, 'rgb_12_444.jpg'), None),
    ],
    'p5' : None,
    'p6' : None,
    'p7' : None,
    'p8' : None,
    'p9' : None,
    'p10' : None,
    'p11' : None,
    'p12' : None,
    'p13' : None,
    'p14' : [

    ],
    'p14sv1' : [
        #(os.path.join(DPROCESS14SV1, 'JPEG-LL_frame1.jpg'), None),
        (os.path.join(DPROCESS14SV1, 'SC_rgb_jpeg_gdcm.jpg'), None),
    ],
    'p15' : None,
    'p16' : None,
    'p17' : None,
    'p18' : None,
    'p19' : None,
    'p20' : None,
    'p21' : None,
    'p22' : None,
    'p23' : None,
    'p24' : None,
    'p25' : None,
    'p26' : None,
    'p27' : None,
    'p28' : None,
    'p29' : None,
}
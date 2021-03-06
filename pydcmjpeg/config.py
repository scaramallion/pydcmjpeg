

JPEG_10918 = (
    'SOF0', 'SOF1', 'SOF2', 'SOF3', 'SOF5',
    'SOF6', 'SOF7', 'SOF9', 'SOF10',
    'SOF11', 'SOF13', 'SOF14', 'SOF15', 
)
JPEG_14495 = ('SOF55', 'LSE', )
JPEG_15444 = ('SOC', )


PARSE_SUPPORTED = {
    '10918' : [
        'Process 1',
        'Process 2',
        'Process 4',
        'Process 14',
    ]
}

DECODE_SUPPORTED = {}
ENCODE_SUPPORTED = {}


ZIGZAG = [ 0,  1,  5,  6, 14, 15, 27, 28,
           2,  4,  7, 13, 16, 26, 29, 42,
           3,  8, 12, 17, 25, 30, 41, 43,
           9, 11, 18, 24, 31, 40, 44, 53,
          10, 19, 23, 32, 39, 45, 52, 54,
          20, 22, 33, 38, 46, 51, 55, 60,
          21, 34, 37, 47, 50, 56, 59, 61,
          35, 36, 48, 49, 57, 58, 62, 63]


10918 JPEG
SOF 0 - Baseline DCT
    Annex F
    8 x 8 block of samples
    DCT-base process
    Source image: 8-bit samples within each component
    Sequential (one frame in image, one or more scan per frame)
        If one component then non-interleaved
        If 2 to 4 components then interleaved within the scan
    Huffman coding: up to 2 AC and up to 2 DC tables per scan
    Decoders shall process scans with 1 to 4 components
    Interleaved and non-interleaved scans

    001 - up to ECS
    color3d_jpeg_baseline_422_frame1 - up to ECS
    huff_simple0 - up to ECS
    grey_8 - up to ECS
    rgb_8_422 - up to ECS
    rgb_8_444 - up to ECS
    SC_rgb_dcmtk_+eb+cr - up to ECS
    SC_rgb_dcmtk_+eb+cy+n1 - up to ECS
    SC_rgb_dcmtk_+eb+cy+n2 - up to ECS
    SC_rgb_dcmtk_+eb+cy+np - up to ECS
    SC_rgb_dcmtk_+eb+cy+s4 - up to ECS
    SC_rgb_jpeg_dcmtk - up to ECS
    SC_rgb_jpeg_lossy_gdcm - up to ECS
    SC_rgb_small_odd_jpeg - up to ECS

SOF 1 - Extended Sequential DCT
    DCT-based process
    Source image: 8-bit or 12-bit samples
    Sequential
    Huffman coding: 4 AC and 4 DC tables
    Decoders shall process scans with 1 to 4 components
    Interleaved and non-interleaved scans

    grey_8 - up to ECS
    grey_12 - up to ECS
    JPEG-lossy - up to ECS
    rgb_8_422 - up to ECS
    rgb_8_444 - up to ECS
    rgb_12_422 - up to ECS
    rgb_12_444 - up to ECS

SOF 3 - Lossless Sequential
    Predictive process
    Source image: 2 to 16 bit samples
    Sequential
    Huffman coding: 4 DC tables
    Decoders shall process scans with 1 to 4 components
    Interleaved and non-interleaved scans

    JPEG-LL_frame1 - up to ECS
    SC_rgb_jpeg_gdcm - up to ECS


14495 JPEG-LS
SOF 55 - JPEG-LS


15444 JPEG 2000


from collections import OrderedDict

from pydcmjpeg.config import JPEG_10918, JPEG_14495, JPEG_15444
from pydcmjpeg.decoders import decode_baseline


class JPEG(object):
    """A representation of an ISO/IEC 10918-1 JPEG file.

    **Non-hierarchical**

    **DCT-based sequential**
    1: Baseline DCT
    2: Extended sequential DCT, Huffman, 8-bit
    3: Extended sequential DCT, arithmetic, 8-bit
    4: Extended sequential DCT, Huffman, 12-bit
    5: Extended sequential DCT, arithmetic, 12-bit

    **DCT-based progressive**
    6: Spectral selection, Huffman, 8-bit
    7: Spectral selection, arithmetic, 8-bit
    8: Spectral selection, Huffman, 12-bit
    9: Spectral seletion, arithmetic, 12-bit
    10: Full progression, Huffman, 8-bit
    11: Full progression, arithmetic, 8-bit
    12: Full progression, Huffman, 12-bit
    13: Full progression, arithmetic, 12-bit

    **Lossless**
    14: Lossless, Huffman, 2 to 16-bit
    15: Lossless, arithmetic, 2 to 16-bit

    **Hierarchical**

    **DCT-based sequential**
    16: Extended sequential DCT, Huffman, 8-bit
    17: Extended sequential DCT, arithmetic, 8-bit
    18: Extended sequential DCT, Huffman, 12-bit
    19: Extended sequential DCT, arithmetic, 12-bit

    **DCT-based progressive**
    20: Spectral selection, Huffman, 8-bit
    21: Spectral selection, arithmetic, 8-bit
    22: Spectral selection, Huffman, 12-bit
    23: Spectral selection, arithmetic, 12-bit
    24: Full progression, Huffman, 8-bit
    25: Full progression, arithmetic, 8-bit
    26: Full progression, Huffman, 12-bit
    27: Full progression, arithmetic, 12-bit

    **Lossless**
    28: Lossless, Huffman, 2 to 16-bit
    29: Lossless, arithmetic, 2 to 16-bit

    """
    def __init__(self, fp, info):
        """Initialise a new JPEG.

        Parameters
        ----------
        fp : file-like
            The file-like that contains the JPEG image.
        info : dict
            The parsed JPEG image.
        """
        self._fp = fp
        self.info = info

        # Used to track whether or not we have decoded the JPEG
        self._array = None
        self._array_id = None

    @property
    def columns(self):
        """Return the number of columns in the image as an int."""
        keys = self.get_keys('SOF')
        if keys:
            return self.info[keys[0]][2]['X']

        raise ValueError(
            "Unable to get the number of columns in the image as no SOFn "
            "marker was found"
        )

    def _decode(self):
        """Decode the JPEG image data in place.

        Raises
        ------
        NotImplementedError
            If the JPEG image data is of a type for which decoding is not
            supported.
        """
        if not self.is_decodable:
            raise NotImplementedError(
                "Unable to decode the JPEG image data as it's of a type "
                "for which decoding is not supported"
            )

        if self.is_process1:
            decoder = decode_baseline
        #elif self.is_process2:
        #    decoder = decode_extended_8
        #elif self.is_process4:
        #    decoder = decode_extended_12
        #elif self.is_process14:
        #    decoder = decode_lossless
        #elif self.is_process14_sv1:
        #    decoder = decode_lossless

        try:
            self._array = decoder(self)
            self._array_id = id(self._array)
        except Exception as exc:
            self._array = None
            self._array_id = None
            raise exc

    def get_keys(self, name):
        """Return a list of keys with marker containing `name`."""
        return [mm for mm in self._keys if name in mm]

    @property
    def is_arithmetic(self):
        raise NotImplementedError

    @property
    def is_baseline(self):
        """Return True if the JPEG is baseline, False otherwise.

        Baseline process
        * DCT-based process
        * Each component of the source image has 8-bit samples
        * Sequential
        * Huffman coding has up to 2 AC and 2 DC tables
        * Decoders shall process scans with 1, 2, 3 and 4 components
        * Interleaved and non-interleaved scans

        Non-hierarchical baseline processes are:
            1
        Hierarchical baseline processes are:
            16, 17, 20, 21, 24, 25.
        """
        return 'SOF0' in self.markers

    @property
    def is_decodable(self):
        """Return True if the JPEG image type is decodable, False otherwise.

        The following processes are decodable:

        * Process 1 (Basline DCT)
        """
        if self.is_process1:
            return True

        return False

    @property
    def is_extended(self):
        """Return True if the JPEG is extended, False otherwise.

        Extended DCT-based processess
        * DCT-based process
        * Each component of the source image has 8- or 12-bit samples
        * Sequential or progressive
        * Huffman or arithmetic coding with up to 4 AC and 4 DC tables
        * Decoders shall process scans with 1, 2, 3 and 4 components
        * Interleaved and non-interleaved scans

        Non-hierarchical extended processes are:
            2, 4
        Hierarchical extended processes are:
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
        """
        extended_markers = ('SOF1', 'SOF9', 'SOF5', 'SOF13')
        if [mm for mm in extended_markers if mm in self.markers]:
            return True

        return False

    @property
    def is_hierarchical(self):
        """Return True if the JPEG is hierarchical, False otherwise.

        Hierarchical processess
        * Multiple frames (non-differential and differential)
        * Uses extended DCT-based or lossless processes
        * Decoders shall process scans with 1, 2, 3 and 4 components
        * Interleaved and non-interleaved scans
        """
        return 'DHP' in self.markers

    @property
    def is_huffman(self):
        raise NotImplementedError

    @property
    def is_lossless(self):
        """Return True if the JPEG is lossless, False otherwise.

        Lossless processess
        * Predictive process (not DCT-based)
        * Each component of the source image P-bit samples (2 <= P <= 16)
        * Sequential
        * Huffman or arithmetic coding with up to 4 DC tables
        * Decoders shall process scans with 1, 2, 3 and 4 components
        * Interleaved and non-interleaved scans

        Non-hierarchical lossless processes are:
            14, 15
        Hierarchical lossless processes are:
            28, 29
        """
        lossless_markers = ('SOF3', 'SOF11') #, 'SOF7', 'SOF15')
        if [mm for mm in lossless_markers if mm in self.markers]:
            return True

        return False

    @property
    def is_non_hierarchical(self):
        """Return True if the JPEG is non-hierarchical, False otherwise."""
        return not self.is_hierarchical

    @property
    def is_process1(self):
        """Return True if the JPEG is Process 1, False otherwise."""
        if self.is_non_hierarchical and self.is_baseline:
            return True

        return False

    @property
    def is_process2(self):
        """Return True if the JPEG is Process 2, False otherwise."""
        try:
            precision = self.precision
        except ValueError:
            return False

        if self.is_non_hierarchical and self.is_extended and precision == 8:
            return True

        return False

    @property
    def is_process4(self):
        """Return True if the JPEG is Process 4, False otherwise."""
        try:
            precision = self.precision
        except ValueError:
            return False

        if self.is_non_hierarchical and self.is_extended and precision == 12:
            return True

        return False

    @property
    def is_process14(self):
        """Return True if the JPEG is Process 14, False otherwise."""
        if 'SOF3' not in self.markers:
            return False

        if self.is_non_hierarchical and self.is_lossless:
            return True

        raise False

    @property
    def is_process14_sv1(self):
        """Return True if the JPEG is Process 14 SV1, False otherwise.

        Returns
        -------
        bool
            True if JPEG is process 14, first-order prediction, selection
            value 1, False otherwise.
        """
        if 'SOF3' not in self.markers:
            return False

        if self.is_hierarchical or not self.is_lossless:
            return False

        if self.selection_value == 1:
            return True

        return False

    @property
    def is_progressive(self):
        raise NotImplementedError

    @property
    def is_sequential(self):
        raise NotImplementedError

    @property
    def _keys(self):
        """Return a list of the info keys, ordered by offset."""
        return sorted(self.info.keys(), key=lambda x: int(x.split('@')[1]))

    @property
    def markers(self):
        """Return a list of the found JPEG markers, ordered by offset."""
        return [mm.split('@')[0] for mm in self._keys]

    @property
    def precision(self):
        """Return the precision of the sample as an int."""
        keys = self.get_keys('SOF')
        if keys:
            return self.info[keys[0]][2]['P']

        raise ValueError(
            "Unable to get the sample precision of the image as no SOFn "
            "marker was found"
        )

    @property
    def rows(self):
        """Return the number of rows in the image as an int."""
        keys = self.get_keys('SOF')
        if keys:
            return self.info[keys[0]][2]['Y']

        raise ValueError(
            "Unable to get the number of rows in the image as no SOFn "
            "marker was found"
        )

    @property
    def samples(self):
        """Return the number of components in the JPEG as an int."""
        keys = self.get_keys('SOF')
        if keys:
            return self.info[keys[0]][2]['Nf']

        raise ValueError(
            "Unable to get the number of components in the image as no SOFn "
            "marker was found"
        )

    @property
    def selection_value(self):
        """Return the JPEG lossless selection value.

        Returns
        -------
        int
            The selection value for the lossless prediction (0-7). 0 shall
            only be used for differential coding in the hierarchical mode of
            operation. 1-3 are one-dimensional predictors and 4-7 are two-
            dimensional predictors.

        Raises
        ------
        ValueError
            If the JPEG is not lossless.
        """
        if not self.is_lossless:
            raise ValueError(
                "Selection value is only available for lossless JPEG"
            )

        sos_markers = [mm for mm in self._keys if 'SOS' in mm]
        return self.info[sos_markers[0]][2]['Ss']

    @property
    def to_array(self):
        """Return the JPEG image data as a numpy ndarray.

        Returns
        -------
        numpy.ndarray
            An ndarray containing the image data.

        Raises
        ------
        NotImplementedError
            If the JPEG is of an unsupported type.
        """
        if self._array and id(self._array) == self._array_id:
            return self._array

        self._decode()

        return self._array

    @property
    def to_bytes(self):
        raise NotImplementedError

    @property
    def uid(self):
        """Return the DICOM UID corresponding to the JPEG.

        Returns
        -------
        str
            The DICOM transfer syntax UID corresponding to the JPEG.

        Raises
        ------
        ValueError
            If the JPEG doesn't correspond to a DICOM transfer syntax.
        """
        if self.is_process1:
            return '1.2.840.10008.1.2.4.50'
        elif self.is_process2 or self.is_process4:
            return '1.2.840.10008.1.2.4.51'
        elif self.is_process14_sv1:
            return '1.2.840.10008.1.2.4.70'
        elif self.is_process14:
            return '1.2.840.10008.1.2.4.57'

        raise ValueError("JPEG doesn't correspond to a DICOM UID")


class JPEGBase(object):
    """Base class for representing a JPEG file."""
    def __init__(self, fp):
        # The file-like that contains the JPEG file
        self._fp = fp
        self.info = {}

    def parse(self):
        pass


class JPEGLS(object):
    """A representation of an ISO/IEC 14495-1 JPEG-LS file."""
    def __init__(self, fp, info):
        self._fp = fp
        self.info = info


class JPEG2000(object):
    """A representation of an ISO/IEC 15444-1 JPEG 2000 file."""
    def __init__(self, fp, info):
        self._fp = fp
        self.info = info


def get_jpeg(fp, info):
    """Return a class representing the JPEG file."""
    markers = [key.split('@')[0] for key in info]
    is_10918 = set(JPEG_10918).intersection(markers)
    is_14495 = set(JPEG_14495).intersection(markers)
    is_15444 = set(JPEG_15444).intersection(markers)

    if ((is_10918 and is_14495 and is_15444)
            or (is_10918 and is_14495)
            or (is_10918 and is_15444)
            or (is_14495 and is_15444)):
        raise ValueError(
            "The JPEG file contains an invalid mix of markers from the "
            "supported protocols"
        )
    elif is_10918:
        return JPEG(fp, info)
    elif is_14495:
        return JPEGLS(fp, info)
    elif is_15444:
        return JPEG2000(fp, info)
    else:
        raise NotImplementedError(
            "The JPEG file is not supported"
        )


class JPEGDict(OrderedDict):
    def __setitem__(self, key, value):
        """Set the item using a Marker.

        Parameters
        ----------
        key : str
            The marker's 'name@offset'.
        value : tuple
            The contents of the marker.
        """
        super(JPEGDict, self).__setitem__(key, value)

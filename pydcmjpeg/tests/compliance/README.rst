ISO/IEC 10918-2 JPEG Compliance Testing
=======================================


Symbols
-------
3.3.6 G: Guaranteed in compressed data
3.3.11 o: optional in compressed data


Table 1 - Marker syntax requirements for non-hierarchical coding processes

+--------+-----------+----------------+
| Marker | Reference | Process        |
|        | in        +---+---+---+----+
|        | 10918-1   | 1 | 2 | 4 | 14 |
+========+===========+===+===+===+====+
| SOI    | B.2.1     | G | G | G | G  |
+--------+-----------+---+---+---+----+
| EOI    | B.2.1     | G | G | G | G  |
+--------+-----------+---+---+---+----+
| RST_m  | B.2.1     | o | o | o | o  |
+--------+-----------+---+---+---+----+
| SOS    | B.2.3     | G | G | G | G  |
+--------+-----------+---+---+---+----+
| DNL    | B.2.5     | o | o | o | o  |
+--------+-----------+---+---+---+----+
| Non-differential frames             |
+--------+-----------+---+---+---+----+
| SOF_0  | B.2.2     | G | - | - | -  |
+--------+-----------+---+---+---+----+
| SOF_1  | B.2.2     | - | G | G | -  |
+--------+-----------+---+---+---+----+
| SOF_3  | B.2.2     | - | - | - | G  |
+--------+-----------+---+---+---+----+
| Tables/miscellaneous                |
+--------+-----------+---+---+---+----+
| DQT    | B.2.4.1   | G | G | G | G  |
+--------+-----------+---+---+---+----+
| DHT    | B.2.4.2   | G | G | G | G  |
+--------+-----------+---+---+---+----+
| DAC    | B.2.4.3   | o | o | o | o  |
+--------+-----------+---+---+---+----+
| DRI    | B.2.4.4   | o | o | o | o  |
+--------+-----------+---+---+---+----+
| COM    | B.2.4.5   | o | o | o | o  |
+--------+-----------+---+---+---+----+
| APP_n  | B.2.4.6   | o | o | o | o  |
+--------+-----------+---+---+---+----+


Notes
~~~~~
The SOF_n markers are non-specific to a process however:

* SOF_0 is always Baseline Sequential DCT (but may be hierarchical or
  non-hierarchical)
* SOF_1 is always Extended Sequential DCT (but may be hierarchical or
  non-hierarchical)
* SOF_3 is always Lossless (but may be hierarchical or non-hierarchical)

Procedure for determining compliance of a DCT-based decoder
-----------------------------------------------------------
1. Decode the supplied compressed image test data using the decoder under test.
2. Calculate the quantized DCT coefficients from the decoded output image
   according to the FDCT and quantization procedures defined in Annex A of
   10918-1, implemented with double precision floating point accuracy.
3. For each quantized coefficient, subtract the reference quantized coefficient
   in the decoder reference test data supplied. 8x8 blocks that were completed
   by extension, or blocks that were added to complete an MCU as defined in
   A.2.4 of 10918-1 shall not be considered. The values of all absolute
   differences shall not exceed one.

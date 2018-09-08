
from pydcmjpeg._markers import MARKERS


class MarkerSegment(object):
    """Lean representation of a JPEG marker segment."""
    def __init__(self, marker, offset):
        """Initialise a new marker segment."""
        self._marker = marker
        self._offset = offset

    @property
    def description(self):
        """Return a description of the marker segment as str."""
        return MARKERS[self.marker][1]

    @property
    def marker(self):
        """Return the marker of the marker segment."""
        return self._marker

    @property
    def name(self):
        """Return the name of the marker segment as str."""
        return MARKERS[self.marker][0]

    @property
    def offset(self):
        """Return the byte offset of the start of the marker segment."""
        return self._offset

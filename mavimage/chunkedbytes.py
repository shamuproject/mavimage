"""ChunkedBytes class
"""
import numbers
import math

class ChunkedBytes:
    """ChunkedBytes class. Edit bytes arrays
    Attributes:
        bytes_item: bytes
        chunk_size: int
    """
    def __init__(self, bytes_item=None, chunk_size=256):
        """Initialize ChunkedBytes class
        Args:
            bytes: bytes
            chunk_size: int
        """
        self._bytes_item = bytes_item
        self._chunk_size = chunk_size

    def __getitem__(self, index):
        """Get item from ChunkedBytes. Raise exception if a tuple is given
        Args:
            index: int
        Returns:
            item: bytes
            """
        if isinstance(index, numbers.Integral):
            item = self._bytes_item[index*self._chunk_size:
                                    (index*self._chunk_size+self._chunk_size)]
            return item
        else:
            raise ValueError("Error: Can only accept an integer value")

    def __setitem__(self, key, byte_sequence):
        """set an item in the byte sequence
        Args:
            key: integer
            byte_sequence: bytes
        """
        first_part = self._bytes_item[:(key*self._chunk_size)]
        last_part = self._bytes_item[((key*self._chunk_size)+self._chunk_size):]
        self._bytes_item = first_part + byte_sequence + last_part

    def __delitem__(self, key):
        """Delete a whole index of the of the ChunkedBytes based on chunk size
        Args:
            key: integer
        """
        first_part = self._bytes_item[:(key * self._chunk_size)]
        last_part = self._bytes_item[((key * self._chunk_size) + self._chunk_size):]
        self._bytes_item = first_part + last_part

    def __len__(self):
        """Find length of indeces of the bytes based on chunk size
        Returns:
            length: int
        """
        return math.ceil(len(self._bytes_item)/self._chunk_size)

    def __add__(self, other):
        """Add bytes or ChunkedBytes. Else raise a NotImplemented exception
        Args:
            other: bytes or ChunkedBytes
        Returns:
            bytes
        """
        if isinstance(other, bytes):
            self._bytes_item = self._bytes_item + other
        else:
            try:
                self._bytes_item = self._bytes_item + other._bytes_item
            except AttributeError:
                raise NotImplementedError
        return self._bytes_item

    def __radd__(self, other):
        """Add with bytes or ChunkedBytes on right of operator.
        Else raise a NotImplemented exception
        Args:
            other: bytes or ChunkedBytes
        Returns:
            bytes
            """
        if isinstance(other, bytes):
            self._bytes_item = other + self._bytes_item
        else:
            try:
                self._bytes_item = other._bytes_item + self._bytes_item
            except AttributeError:
                raise NotImplementedError
        return self._bytes_item

    def zeros(self, chunks, chunk_size=256):
        """Return zeros of length chunks*chunk_size
        Args:
             chunks: int
             chunk_size: int
        """
        zero_array = 0x00 * chunk_size
        for i in range(0, chunks-1):
            zero_array = zero_array + (0x00 * chunk_size)
        return zero_array

    def insert(self, index, chunk):
        """Insert chunks into bytes
        Args:
            index: int
            chunk: bytes
        """
        first_part = self._bytes_item[:index*self._chunk_size]
        last_part = self._bytes_item[self._chunk_size*index:]
        self._bytes_item = first_part + chunk + last_part

    def flat(self):
        """Returns all bytes as one array
        Returns:
             bytes
        """
        return self._bytes_item

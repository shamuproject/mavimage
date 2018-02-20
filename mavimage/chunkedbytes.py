"""ChunkedBytes class.
Takes
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
        #bytes: bytes, chunk_size: int
        self._bytes_item = bytes_item
        self._chunk_size = chunk_size

    def __getitem__(self, index):
        #item: bytes
        if isinstance(index, numbers.Integral):
            item = self._bytes_item[index*self._chunk_size:
                                    (index*self._chunk_size+self._chunk_size)]
            return item
        else:
            print("Error: Can only accept an integer value")

    def __setitem__(self, key, byte_sequence):
        # key: index, value: bytes
        self._bytes_item[key*self._chunk_size:
                        (key*self._chunk_size)+self._chunk_size] = byte_sequence

    def __delitem__(self, key):
        # key: index, bytes_sequence: bytes
        del(self._bytes_item[(key*self._chunk_size):
                                (key*self._chunk_size)+self._chunk_size])

    def __len__(self):
        # length: int
        return math.ceil(len(self._bytes_item)/self._chunk_size)

    def __add__(self, other):
        # other: bytes or ChunkedBytes

    def __radd__(self, other):
        # looks at left object to see if will work with object on right
        # if not, throw Error: NotImplemented
        # give thing on left to right to see if it will work
        # other: bytes or ChunkedBytes

    def zeros(self, chunks, chunk_size=256):
        #chunks: int, chunk_size: int

    def insert(self, index, chunk):
        # insert at index
        # chunks: bytes
        save_chunks = self._bytes_item[index:]
        self._bytes_item[index] = chunk
        self._bytes_item[(index+1):] = save_chunks

    def flat(self):
        # value: bytes
        return value
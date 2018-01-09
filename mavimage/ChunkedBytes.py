import MavtableSequence
'''
ChunkedBytes class
Attributes:
    byes:bytes
    chunk_size:int
'''

class ChunkedBytes:

    def __init__(self, bytes=None, chunk_size=256):
        # bytes: bytes, chunk_size: int

    def __getitem__(self, item):
        # item: bytes
        return item

    def __setitem__(self, key, value):
        # key, value

    def __delitem__(self, key):
        # key

    def __len__(self):
        length = 0
        # length: int
        return length

    def __add__(self, other):
        # other: bytes or ChunkedBytes

    def __radd__(self, other):
        # other: bytes or ChunkedBytes

    def zeros(self, chunks, chunk_size=256):
        # chunks: int, chunk_size: int

    def insert(self, chunks):
        #chunks: bytes

    def flat(self):
        #value: bytes
        return value
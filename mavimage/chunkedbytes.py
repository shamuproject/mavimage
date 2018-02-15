'''
ChunkedBytes class
Attributes:
    byes:bytes
    chunk_size:int
'''

class ChunkedBytes:

    def __init__(self, bytes_item=None, chunk_size=256):
        # bytes: bytes, chunk_size: int
        self.bytes_item = bytes_item
        self.chunk_size = chunk_size

    def __getitem__(self, item):
        # item: bytes
        item_index = self.bytes_item.index(item)
        return item_index

    def __setitem__(self, key, value):
        # key, value
        bytes_item[key] = value

    def __delitem__(self, key):
        # key
        del(self.bytes_item[key])


    def __len__(self):
        # length: int
        return len(self.bytes_item)

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
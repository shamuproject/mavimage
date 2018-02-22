from mavimage.chunkedbytes import ChunkedBytes
import pytest

def test_init():
    bytes_original = bytes(b"abc")
    chunk_size_original = 700
    chkbt = ChunkedBytes(bytes_original, chunk_size_original)
    assert chkbt._bytes_item == bytes_original
    assert chkbt._chunk_size == chunk_size_original

    chkbt2 = ChunkedBytes(bytes_original)
    assert chkbt2._bytes_item == bytes_original
    assert chkbt2._chunk_size == 256


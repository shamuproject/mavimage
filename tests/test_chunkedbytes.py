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

def test_get():
    """test individual bytes, less than the default size, default size, and greater
    than default size
    """
    bytes_original = bytes(b"abc")
    chkbt = ChunkedBytes(bytes_original, 1)
    assert chkbt[0] == bytes(b"a")
    assert chkbt[1] == bytes(b"b")
    assert chkbt[2] == bytes(b"c")

    bytes_original = bytes(b"aaabbbcccdddeee")
    chkbt = ChunkedBytes(bytes_original, 3)
    assert chkbt[0] == bytes(b"aaa")
    assert chkbt[1] == bytes(b"bbb")
    assert chkbt[2] == bytes(b"ccc")
    assert chkbt[3] == bytes(b"ddd")
    assert chkbt[4] == bytes(b"eee")

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    assert chkbt[0] == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuv")
    assert chkbt[1] == bytes(b"wxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original, 260)
    assert chkbt[0] == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    assert chkbt[1] == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")


def test_set():

    bytes_original = bytes(b"aaabbbcccdddeee")
    chkbt = ChunkedBytes(bytes_original, 3)
    assert chkbt[0] == bytes(b"aaa")
    assert chkbt[1] == bytes(b"bbb")
    assert chkbt[2] == bytes(b"ccc")
    assert chkbt[3] == bytes(b"ddd")
    assert chkbt[4] == bytes(b"eee")

    chkbt[0] = bytes(b"eee")
    chkbt[1] = bytes(b"ddd")
    chkbt[2] = bytes(b"ccc")
    chkbt[3] = bytes(b"bbb")
    chkbt[4] = bytes(b"aaa")
    assert chkbt[4] == bytes(b"aaa")
    assert chkbt[3] == bytes(b"bbb")
    assert chkbt[2] == bytes(b"ccc")
    assert chkbt[1] == bytes(b"ddd")
    assert chkbt[0] == bytes(b"eee")

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    chkbt[0] = bytes(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert chkbt._bytes_item == bytes(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                           b"wxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")



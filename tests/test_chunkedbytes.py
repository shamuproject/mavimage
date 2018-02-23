"""Test ChunkedBytes class
"""
from mavimage.chunkedbytes import ChunkedBytes
import pytest

def test_init():
    """Test initialization for chunk size and bytes
    """
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
    than default size. Assert error for tuple assignment
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

    with pytest.raises(ValueError) as excinfo:
        chkbt[0:1]
    assert str(excinfo.value) == "Error: Can only accept an integer value"


def test_set():
    """Test placing at beginning, end, and middle of bytes
    """
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


    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    chkbt[1] = bytes(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert chkbt._bytes_item == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvaaaa"
                           b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

def test_delete():
    """Test deleting in beginning, middle, and end of default
    and less than default sizes
    """
    bytes_original = bytes(b"aaabbbcccdddeee")
    chkbt = ChunkedBytes(bytes_original, 3)
    del(chkbt[0])
    assert (chkbt._bytes_item == bytes(b"bbbcccdddeee"))
    del (chkbt[1])
    assert (chkbt._bytes_item == bytes(b"bbbdddeee"))
    del (chkbt[2])
    assert (chkbt._bytes_item == bytes(b"bbbddd"))
    del (chkbt[1])
    assert (chkbt._bytes_item == bytes(b"bbb"))
    del (chkbt[0])
    assert (chkbt._bytes_item == bytes(b""))

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    del(chkbt[1])
    assert chkbt._bytes_item ==bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuv")

def test_length():
    """Test for proper index length using default and less
    than default sizes
    """
    bytes_original = bytes(b"aaabbbcccdddeee")
    chkbt = ChunkedBytes(bytes_original, 3)
    assert len(chkbt) == 5

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    assert len(chkbt) == 2

def test_add():
    """Test adding bytes and ChunkedBytes together for default
    and less than default size
    """
    bytes_original = bytes(b"aaabbbcccdddeee")
    bytes_add = bytes(b"aaa")
    chkbt = ChunkedBytes(bytes_original, 3)
    chkbt2 = ChunkedBytes(bytes_original, 3)
    add = chkbt._bytes_item + bytes_add
    assert add == bytes(b"aaabbbcccdddeeeaaa")
    add2 = chkbt + bytes_add
    assert add2 == bytes(b"aaabbbcccdddeeeaaa")
    add3 = chkbt + chkbt2
    assert add3 == bytes(b"aaabbbcccdddeeeaaaaaabbbcccdddeee")

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    bytes_add = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    add = chkbt._bytes_item + bytes_add
    assert add == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        )
    chkbt = ChunkedBytes(bytes_original)
    add2 = chkbt + bytes_add
    assert add2 == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        )
    with pytest.raises(NotImplementedError) as excinfo:
        add3 = chkbt + 45
    assert str(excinfo.value) == ""

def test_radd():
    """Test adding bytes and ChunkedBytes together on right
    for default and less than default size
    """
    bytes_original = bytes(b"aaabbbcccdddeee")
    bytes_add = bytes(b"aaa")
    chkbt = ChunkedBytes(bytes_original, 3)
    add = bytes_add + chkbt._bytes_item
    assert add == bytes(b"aaaaaabbbcccdddeee")
    add2 = bytes_add + chkbt
    assert add2 == bytes(b"aaaaaabbbcccdddeee")

    chkbt2 = ChunkedBytes(bytes_original, 3)
    add = chkbt._bytes_item + bytes_add
    add3 = chkbt2 + chkbt
    assert add3 == bytes(b"aaabbbcccdddeeeaaaaaabbbcccdddeee")

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    bytes_add = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                      b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                      b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                      b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                      b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                      b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    add = chkbt._bytes_item + bytes_add
    assert add == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                        )

    add2 = chkbt + bytes_add
    assert add2 == bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                         )

    with pytest.raises(NotImplementedError) as excinfo:
        add3 = 45 + chkbt
    assert str(excinfo.value) == ""

def test_zeros():
    """Test returning zero byte array for default and nondefault
    sizes
    """
    bytes_original = bytes(b"aaabbbcccdddeee")
    chkbt = ChunkedBytes(bytes_original, 3)
    assert chkbt.zeros(2, 1) == 0x0000
    assert chkbt.zeros(1, 256) == (0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x00000000000000000000000000000000000000000000)
    assert chkbt.zeros(2, 256) == (0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x00000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x0000000000000000000000000000000000000000000000000000 +
                                   0x00000000000000000000000000000000000000000000
                                   )

def test_insert():
    """Test inserting into middle, beginning, and end
    """
    bytes_original = bytes(b"aaabbbcccdddeee")
    chkbt = ChunkedBytes(bytes_original, 3)
    chkbt.insert(1, b"www")
    assert chkbt._bytes_item == bytes(b"aaawwwbbbcccdddeee")
    chkbt.insert(4, b"ccc")
    assert chkbt._bytes_item == bytes(b"aaawwwbbbccccccdddeee")
    chkbt.insert(0, b"kpll")
    assert chkbt._bytes_item == bytes(b"kpllaaawwwbbbccccccdddeee")
    chkbt.insert(9, b"m")
    assert chkbt._bytes_item == bytes(b"kpllaaawwwbbbccccccdddeeem")

def test_flat():
    """Test returning bytes for default and nondefault sizes
    """
    bytes_original = bytes(b"aaabbbcccdddeee")
    chkbt = ChunkedBytes(bytes_original, 3)
    assert chkbt.flat() == bytes_original

    bytes_original = bytes(b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
                           b"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
    chkbt = ChunkedBytes(bytes_original)
    assert chkbt.flat() == bytes_original
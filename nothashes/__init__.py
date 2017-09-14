"""
nothashes
"""

from abc import ABCMeta
from zlib import crc32 as _crc32
from zlib import adler32 as _adler32
from copy import deepcopy
from sys import byteorder

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "1.0.2"


class hashwrap(metaclass=ABCMeta):
    """
    An ABC for mapping the zlib interface to the hashlib interface

    Because the zlib classes operate primarily in ints we hold onto that
    representation as well, in the checksum property, rather than bothering
    with constant conversions between bytes, ints, and strs.
    """

    def __init__(self, inner_func, hashable=None):
        """
        Create a new instance of the wrapping class

        __Args__

        1. inner_func (callable): The inner function that should
            operate on the bytes.

        __KWArgs__

        * hashable (bytes/bytes iter): A thing to "hash"

        """
        self.checksum = None
        self._inner_func = inner_func
        if hashable:
            self.update(hashable)

    def update(self, hashable):
        """
        Facilitates peicemeal operations when you can't get the whole thing
        you want "hashed" into memory all in one go (or don't want to).

        If called with no standing result begins the "hash"-ing operation with
        that input.

        __Args__

        1. hashable (bytes/byte iter): Bytes to append to the standing
            result
        """
        if self.checksum is not None:
            self.checksum = self._inner_func(hashable, self.checksum)
        else:
            self.checksum = self._inner_func(hashable)

    def digest(self):
        return self.checksum.to_bytes(4, byteorder)

    def hexdigest(self):
        return str(self.checksum)

    def copy(self):
        return deepcopy(self)


class crc32(hashwrap):
    digest_size = 4
    block_size = 4
    name = "crc32"

    def __init__(self, hashable=None):
        super().__init__(_crc32, hashable)


class adler32(hashwrap):
    digest_size = 4
    block_size = 4
    name = "adler32"

    def __init__(self, hashable=None):
        super().__init__(_adler32, hashable)

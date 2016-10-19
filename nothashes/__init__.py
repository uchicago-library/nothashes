from abc import ABCMeta, abstractmethod
from zlib import crc32 as _crc32
from zlib import adler32 as _adler32
from copy import deepcopy
from sys import byteorder


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
        self._checksum = None
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

    def get_checksum(self):
        return self._checksum

    def set_checksum(self, x):
        self._checksum = x

    def get_digest_size(self):
        raise NotImplementedError()

    def get_block_size(self):
        raise NotImplementedError()

    def get_name(self):
        # Note: This isn't a suitable parameter to hashlib.hash.new(), because
        # hashlib has no idea about this module
        raise NotImplementedError()

    @property
    def checksum(self):
        return self._checksum

    @checksum.setter
    def checksum(self, x):
        self._checksum = x

    @property
    @abstractmethod
    def digest_size(self):
        pass

    @property
    @abstractmethod
    def block_size(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass


class crc32(hashwrap):
    def __init__(self, hashable=None):
        super().__init__(_crc32, hashable)

    @property
    def digest_size(self):
        return 4

    @property
    def block_size(self):
        return 4

    @property
    def name(self):
        return "crc32"


class adler32(hashwrap):
    def __init__(self, hashable=None):
        super().__init__(_adler32, hashable)

    @property
    def digest_size(self):
        return 4

    @property
    def block_size(self):
        return 4

    @property
    def name(self):
        return "adler32"

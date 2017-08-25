import unittest
from os import urandom
from zlib import crc32 as zlib_crc32
from zlib import adler32 as zlib_adler32

from nothashes import crc32, adler32


class RandomizedTests(unittest.TestCase):
    def testRandomCrc(self):
        for _ in range(10):
            data = urandom(256)
            self.assertEqual(
                str(zlib_crc32(data)), crc32(data).hexdigest()
            )
        for _ in range(10):
            data = urandom(256)
            hasher = crc32()
            hasher.update(data[:128])
            hasher.update(data[128:])
            self.assertEqual(
                str(zlib_crc32(data)), hasher.hexdigest()
            )

    def testRandomAdler(self):
        for _ in range(10):
            data = urandom(256)
            self.assertEqual(
                str(zlib_adler32(data)), adler32(data).hexdigest()
            )
        for _ in range(10):
            data = urandom(256)
            hasher = adler32()
            hasher.update(data[:128])
            hasher.update(data[128:])
            self.assertEqual(
                str(zlib_adler32(data)), hasher.hexdigest()
            )


class InterfaceTests(unittest.TestCase):
    def testInterface(self):
        impls = [adler32, crc32]
        for x in impls:
            i = x()
            self.assertTrue(isinstance(i.name, str))
            self.assertTrue(isinstance(i.digest_size, int))
            self.assertTrue(isinstance(i.block_size, int))
            i.update(b"1234")
            self.assertTrue(isinstance(i.hexdigest(), str))
            self.assertTrue(isinstance(i.digest(), bytes))
            c = i.copy()
            self.assertEqual(i.hexdigest(), c.hexdigest())
            c.update(b"5678")
            self.assertFalse(i.hexdigest() == c.hexdigest())


if __name__ == "__main__":
    unittest.main()

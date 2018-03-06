# nothashes

v1.0.3

[![Build Status](https://travis-ci.org/uchicago-library/nothashes.svg?branch=master)](https://travis-ci.org/uchicago-library/nothashes) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/nothashes/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/nothashes?branch=master)

Wrapper classes for zlib.crc32 and zlib.alder32 that make them behave like hashlib classes.

# Usage Example
```python
>>> from nothashes import crc32, adler32
>>> crcer = crc32()
>>> crcer.update(b'1234')
>>> crcer.digest()
b'\x9b\xe3\xe0\xa3'
>>> crcer.hexdigest()
'2615402659'
>>> crcer.update(b'5678')
>>> crcer.digest()
b'\x9a\xe0\xda\xaf'
>>> crcer.hexdigest()
'2598427311'
>>> crcer_again = crc32(b'12345678')
>>> crcer_again.hexdigest()
'2598427311'
>>> adlerer = adler32()
>>> adlerer.update(b'1234')
>>> adlerer.digest()
b'\x01\xf8\x00\xcb'
>>> adlerer.hexdigest()
'33030347'
>>> adlerer.update(b'5678')
>>> adlerer.digest()
b'\x07@\x01\xa5'
>>> adlerer.hexdigest()
'121635237'
>>> adlerer_again = adler32(b'12345678')
>>> adlerer_again.hexdigest()
'121635237'
>>> some_file_crc = crc32()
>>> with open('some_test_file.txt', 'rb') as f:
...     data = f.read(1)
...     while data:
...             some_file_crc.update(data)
...             data = f.read(1)
... 
>>> some_file_crc.hexdigest()
'3497126867'
```

# Author
Brian Balsamo <brian@brianbalsamo.com>

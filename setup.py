from setuptools import setup
from setuptools import find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name = 'nothashes',
    version="1.0.0",
    description = 'Wrapper classes provided hashlib like behavior for ' + \
    'zlib.crc32 and zlib.alder32',
    long_description = readme(),
    author = "Brian Balsamo",
    author_email = "balsamo@uchicago.edu",
    packages = find_packages(
        exclude = [
            "build",
            "dist",
            "nothashes.egg-info"
        ]
    ),
)

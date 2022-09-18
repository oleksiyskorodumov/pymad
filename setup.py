#!/usr/bin/env python

"""Setup script for the MAD module distribution."""

import setuptools
import distutils.core

VERSION_MAJOR = 0
VERSION_MINOR = 2
PYMAD_VERSION = str(VERSION_MAJOR) + '.' + str(VERSION_MINOR)


DEFINES = [
    ('VERSION_MAJOR', VERSION_MAJOR),
    ('VERSION_MINOR', VERSION_MINOR),
    ('VERSION', '"%s"' % PYMAD_VERSION)
]

MADMODULE = distutils.core.Extension(
    name='mad',
    sources=['src/madmodule.c', 'src/pymadfile.c', 'src/xing.c'],
    define_macros=DEFINES,
    include_dirs=['libmad'],
    library_dirs=['libmad/.libs'],
    libraries=['mad']
)

project_urls = {
    'GitHub': 'https://github.com/oleksiyskorodumov/pymad'
}

classifiers=[
    'Topic :: Multimedia :: Sound/Audio :: Conversion',
    'Programming Language :: Python :: 3 :: Only',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Operating System :: POSIX :: Linux'
]

long_description = "pymad is a Python module that allows Python programs to use the MPEG Audio Decoder library. " \
                   "pymad provides a high-level API, which reading PCM data from MPEG audio streams."

setuptools.setup(  # Distribution metadata
    name='pylibmad',
    version=PYMAD_VERSION,
    description='A Python wrapper for the MPEG Audio Decoder library.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Jamie Wilkinson',
    author_email='jaq@spacepants.org',
    project_urls=project_urls,
    license='GPL',
    keywords='libmad mp3 decoder',
    classifiers=classifiers,
    python_requires='>=3.5',
    ext_modules=[MADMODULE]
)

pymad - a Python wrapper for the MPEG Audio Decoder library
===========================================================

![ci](https://github.com/oleksiyskorodumov/pymad/workflows/CI/badge.svg)
pymad is a Python module that allows Python programs to use the MPEG Audio Decoder library. pymad provides a high-level API, similar to the pyogg module, which makes reading PCM data from MPEG audio streams a piece of cake.

MAD is available at http://www.mars.org/home/rob/proj/mpeg/

Access this module via `import mad`.  To decode
an mp3 stream, you'll want to create a `mad.MadFile` object and read data from
that.  You can then write the data to a sound device.  See the example
program in `test/` for a simple mp3 player that uses the `python-pyao` wrapper around libao for the sound
device.

pymad wrapper isn't as low level as the C MAD API is, for example, you don't
have to concern yourself with fixed point conversion -- this was done to
make pymad easy to use.

```python
import sys

import ao
import mad

mf = mad.MadFile(sys.argv[1])
dev = ao.AudioDevice(0, rate=mf.samplerate())
while 1:
    buf = mf.read()
    if buf is None:  # eof
        break
    dev.play(buf, len(buf))
```

# Build libmad
## Download libmad
```sh
mkdir -p libmad
curl -L https://github.com/oleksiyskorodumov/libmad/tarball/master | tar -xzf - -C libmad --strip-components 1
```

## Build libmad
```sh
cd libmad
autoreconf -fi
./configure --prefix=/usr --disable-static

make
```

# Install
## Install to active environment
```sh
python setup.py build
python setup.py install
```

## Create .whl package
```sh
python" setup.py bdist_wheel -d dist
```

### Install from .whl package
```sh
pip install dist/pymad-<version>-<palatform>.whl
```

#!/bin/bash

set -e -x

# Change to the source directory
cd "$( dirname -- "$0"; )/../../"

# download libmad
mkdir -p libmad
curl -L https://github.com/oleksiyskorodumov/libmad/tarball/master | tar -xzf - -C libmad --strip-components 1

# build libmad
cd libmad
autoreconf -fi
./configure --prefix=/usr --disable-static

make

# setup .whl
cd ..
for PYBIN in /opt/python/*/bin; do
    if [[ $PYBIN = *"cp27"* ]]; then
        continue
    fi
    "${PYBIN}/python" setup.py bdist_wheel -d dist
done
for whl in dist/*.whl; do
    auditwheel repair "$whl" -w dist/
    rm "$whl"
done

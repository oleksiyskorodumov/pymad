#!/usr/bin/env python

from __future__ import print_function

import os
import sys

def msg_checking(msg):
    print("Checking {}... ".format(msg), end='')

def execute(cmd, display=0):
    if display:
        print(cmd)
    return os.system(cmd)

def run_test(inp, flags=''):
    try:
        tmp = open('_temp.c', 'w')
        tmp.write(inp)
        tmp.close()
        compile_cmd = '%s -o _temp _temp.c %s' % (os.environ.get('CC', 'cc'),
                                                  flags)
        if not execute(compile_cmd):
            execute('./_temp')
    finally:
        execute('rm -f _temp.c _temp')

MAD_TEST_PROGRAM = '''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mad.h>

int main ()
{
  system("touch conf.madtest");
  return 0;
}
'''

def find_mad(mad_prefix='/usr/local', enable_madtest=1):
    """A rough translation of mad.m4"""

    mad_libs = []

    mad_include_dir = mad_prefix + '/include'
    mad_lib_dir = mad_prefix + '/lib'
    mad_libs = 'mad'

    msg_checking('for MAD')

    if enable_madtest:
        execute('rm -f conf.madtest', 0)

        try:
            run_test(MAD_TEST_PROGRAM, flags="-I" + mad_include_dir)
            if not os.path.isfile('conf.madtest'):
                raise RuntimeError("Did not produce output")
            execute('rm conf.madtest', 0)

        except:
            print("test program failed")
            return None

    print("success")

    return {'mad_libs' : mad_libs,
            'mad_lib_dir' : mad_lib_dir,
            'mad_include_dir' : mad_include_dir}

ENDIAN_TEST_PROGRAM = '''
#include <stdio.h>

int litend() {
  int i = 0;
  ((char *)(&i))[0] = 1;
  return(i == 1);
}

int bigend() {
  return !litend();
}

int main() {
  if (litend()) {
    system("touch little.endiantest");
  } else {
    system("touch big.endiantest");
  }
}
'''

def check_endian(enable_endiantest=1):
    """check the system for endianness"""

    bigendian = 1

    msg_checking('endianness')

    if enable_endiantest:
        try:
            run_test(ENDIAN_TEST_PROGRAM)
            if os.path.isfile("little.endiantest"):
                bigendian = 0
            elif os.path.isfile("big.endiantest"):
                bigendian = 1
            else:
                raise RuntimeError("Did not produce output")
            execute("rm -f little.endiantest big.endiantest", 0)
        except:
            print("test program failed")
            return None

    print("success")

    return bigendian


def write_data(data):
    setup_file = open('Setup', 'w')
    for item in list(data.items()):
        setup_file.write('%s = %s\n' % item)
    setup_file.close()
    print("Wrote Setup file")

def print_help():
    print('''%s
    --prefix      Give the prefix in which MAD was installed.''' % sys.argv[0])
    sys.exit(0)

def parse_args():
    data = {}
    argv = sys.argv
    for pos in range(len(argv)):
        if argv[pos] == '--help':
            print_help()
        if argv[pos] == '--prefix':
            pos = pos + 1
            if len(argv) == pos:
                print("Prefix needs an argument")
                sys.exit(1)
            data['prefix'] = argv[pos]

    return data

def main():
    args = parse_args()
    prefix = args.get('prefix', '/usr/local')

    data = find_mad(mad_prefix=prefix)
    if not data:
        print("Config failure")
        sys.exit(1)
    if check_endian() == 1:
        data["endian"] = "big"
    else:
        data["endian"] = "little"
    write_data(data)

if __name__ == '__main__':
    main()

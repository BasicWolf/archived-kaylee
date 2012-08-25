#!/usr/bin/env python

import os
import sys
import argparse
import subprocess
import shutil
import glob
import kaylee

FILES_COUNT = 2

def get_client_dir():
    return os.path.abspath(os.path.join(os.path.dirname(kaylee.__file__),
                                        'client'))


def main():
    parser = argparse.ArgumentParser(description='Kaylee client builder.')
    parser.add_argument('dir', help="Directory to which Kaylee client files are collected.")
    parser.add_argument('-b', '--build', action='store_true')

    args = parser.parse_args()


    if args.build:
        p = subprocess.Popen('make', cwd=client_dir, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        data, err = p.communicate()

    dest_dir = os.path.abspath(args.dir)
    if not os.path.exists(dest_dir):
        print("Creating directory...")
        os.makedirs(dest_dir)

    client_dir = get_client_dir()

    print("Copying files...")

    counter = 0
    for f in glob.iglob(os.path.join(client_dir, '*.js')):
        shutil.copy(f, dest_dir)
        counter += 1

    if counter != FILES_COUNT:
        print('Error copying files: files are probably absent')
        sys.exit(1)

    print("Finished.")


if __name__ == '__main__':
    main()

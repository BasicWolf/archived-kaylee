#!/usr/bin/pyhton

import os
import sys
import argparse
import subprocess
import shutil
import glob

parser = argparse.ArgumentParser(description='Kaylee client builder.')
parser.add_argument('dir', help="Directory to which Kaylee client files are gathered.")
parser.add_argument('-l', '--local', action='store_true')
parser.add_argument('-b', '--build', action='store_true')

args = parser.parse_args()

if args.local:
    client_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              '../client'))
else:
    import kaylee
    client_dir = os.path.abspath(os.path.join(os.path.dirname(kaylee.__file__),
                                              '../client'))

if args.build:
    p = subprocess.Popen('make', cwd=client_dir, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    data, err = p.communicate()


dest_dir = os.path.abspath(args.dir)
if not os.path.exists(dest_dir):
    print("Creating directory...")
    os.makedirs(dest_dir)

print("Copying files...")
for f in glob.iglob(os.path.join(client_dir, '*.js')):
    shutil.copy(f, dest_dir)

print("Finished.")

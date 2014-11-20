"""
Script that calls `convert_to_md` on every file in this directory (relative paths)
"""
from glob import glob
from subprocess import call

json_files = glob('*.json')
for f in json_files:
    call(['python', 'convert_to_md.py', f])

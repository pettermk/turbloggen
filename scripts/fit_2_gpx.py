from fit2gpx import Converter

from pathlib import Path

import re

import sys

def fit_to_gpx(folder: str):
    conv = Converter()
    for f in Path(folder).rglob('*.fit'):
        dest = re.sub(r'fit$', 'gpx', str(f))
        print(f'Creating ${dest} from {str(f)}')
        gpx = conv.fit_to_gpx(str(f), dest)



if __name__ == '__main__':
    folder = sys.argv[1]
    fit_to_gpx(folder)




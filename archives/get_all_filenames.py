import glob
import re

GLOB = '/Users/tom/Downloads/bbcsfx-pages/*.htm'
FILES = list(glob.glob(GLOB))
PATTERN = re.compile(r'assets/(\d+.wav)')


def get_all_filenames():
    results = set()
    for f in FILES:
        results.update(PATTERN.findall(open(f).read()))

    for i in sorted(results):
        print(i)


if __name__ == '__main__':
    get_all_filenames()

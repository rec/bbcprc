import os
from . import files

TIMEOUT = 2

ROOT_DIR = '/Volumes/Bach/disks/bbcsfx'
SOURCE_DIR = os.path.join(ROOT_DIR, 'source')
METADATA_DIR = os.path.join(ROOT_DIR, 'metadata')
CLIP_DIR = os.path.join(ROOT_DIR, 'clips')

URL_ROOT = 'http://bbcsfx.acropolis.org.uk/assets'
ALL_FILENAMES = 'results/all_filenames.txt'
DURATION_FILE = 'results/durations.json'

FRAME_RATE = 44100

TOTAL_LENGTH = 75934860815
TOTAL_LENGTH_FACTORS = 5, 11, 10973, 125821


def source(fname):
    return os.path.join(SOURCE_DIR, fname)


def metadata(fname):
    return os.path.join(METADATA_DIR, fname + '.json')


def clip(fname):
    return os.path.join(CLIP_DIR, fname)


def shard(project_name, index, level=0):
    basename = '%d-%d.npy' % (index, level)
    return os.path.join(ROOT_DIR, project_name, 'shards', basename)


def all_files(fname):
    return source(fname), metadata(fname), clip(fname)


def metadata_files():
    return sorted(files.with_suffix(METADATA_DIR, '.json'))


def source_files():
    return sorted(files.with_suffix(SOURCE_DIR, '.wav'))


def clip_files():
    return sorted(files.with_suffix(CLIP_DIR, '.wav'))

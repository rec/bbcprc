import os

TIMEOUT = 2

ROOT_DIR = '/Volumes/Bach/disks/bbcsfx'
SOURCE_DIR = os.path.join(ROOT_DIR, 'source')
METADATA_DIR = os.path.join(ROOT_DIR, 'metadata')
CLIPS_DIR = os.path.join(ROOT_DIR, 'clips')

URL_ROOT = 'http://bbcsfx.acropolis.org.uk/assets'
ALL_FILENAMES = 'results/all_filenames.txt'
DURATION_FILE = 'results/durations.json'

FRAME_RATE = 44100


def files(fname):
    return (
        os.path.join(SOURCE_DIR, fname),
        os.path.join(METADATA_DIR, fname + '.json'),
        os.path.join(CLIP_DIR, fname))

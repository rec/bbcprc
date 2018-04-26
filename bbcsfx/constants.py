import os

TIMEOUT = 2

SOURCE_DIR = '/Volumes/Bach/disks/bbcsfx'
METADATA_DIR = 'results/metadata'
CLIP_DIR = '/Volumes/Bach/disks/bbcsfx_clips'
DIRECTORIES = SOURCE_DIR, METADATA_DIR, CLIP_DIR

URL_ROOT = 'http://bbcsfx.acropolis.org.uk/assets'
ALL_FILENAMES = 'results/all_filenames.txt'
DURATION_FILE = 'results/durations.json'

FRAME_RATE = 44100


def files(fname):
    return (
        os.path.join(SOURCE_DIR, fname),
        os.path.join(METADATA_DIR, fname + '.json'),
        os.path.join(CLIP_DIR, fname))

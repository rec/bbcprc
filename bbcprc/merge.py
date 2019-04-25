"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import sys, yaml
from pathlib import Path
from . files import read_frames, wave_writer
from . import constants
STOP_AFTER = 5


def merge(outfile, files, index_out=sys.stdout):
    def records(out):
        for f in files:
            yield f, out.tell()
            frames, channels = read_frames(f)
            if channels == 1:
                frames = bytes(mono_to_stereo(frames))
            out.writeframes(frames)
        yield '(END)', out.tell()

    with wave_writer(outfile) as out:
        yaml.safe_dump_all(records(out), index_out)


def mono_to_stereo(frames):
    for frame in zip(*[iter(frames)] * 2):
        yield from frame + frame


def sorted_files():
    def g():
        for i, f in enumerate(yaml.safe_load_all(open('results/census.yml'))):
            if STOP_AFTER and i >= STOP_AFTER:
                break
            yield f['nframes'], f['filename']

    for _, filename in sorted(g()):
        yield filename


def master_merge():
    with open(constants.CORPUS_INDEX, 'w') as fp:
        merge(constants.CORPUS, sorted_files(), fp)


if __name__ == '__main__':
    master_merge()

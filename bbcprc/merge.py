"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import sys, yaml
from pathlib import Path
from . files import read_frames, wave_writer
STOP_AFTER = 0


def merge(outfile, files=None):
    if files is None:
        files = sorted_files()

    def records(out):
        for f in files:
            yield f, out.tell()
            frames, channels = read_frames(f)
            if channels == 1:
                frames = bytes(mono_to_stereo(frames))
            out.writeframes(frames)
        yield '(END)', out.tell()

    with wave_writer(outfile) as out:
        yaml.safe_dump_all(records(out), sys.stdout)


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


if __name__ == '__main__':
    if True:
        merge(sys.argv[1])

    elif True:
        for i in sorted_files():
            print(i)
    else:
        out, *files = sys.argv[1:]
        assert files, 'No files'
        merge(out, files)

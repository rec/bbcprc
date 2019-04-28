"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import sys, yaml
from pathlib import Path
from . elapsed_bar import ElapsedBar
from . files import read_frames, wave_writer
from . import constants

STOP_AFTER = None


def merge(outfile, files, index_out=sys.stdout):
    def records(out):
        bar = ElapsedBar(max=len(files))
        for f in files:
            yield f, out.tell()
            bar.next_item(Path(f).name)
            frames, channels = read_frames(f)
            if channels == 1:
                frames = bytes(mono_to_stereo(frames))
            out.writeframes(frames)
        yield '(END)', out.tell()
        bar.finish()

    with wave_writer(outfile) as out:
        yaml.safe_dump_all(records(out), index_out)


def mono_to_stereo(frames):
    for frame in zip(*[iter(frames)] * 2):
        yield from frame + frame


def sorted_files():
    def g():
        for i, f in enumerate(yaml.safe_load_all(open('results/census.yml'))):
            yield f['nframes'], f['filename']

    return [f for (_, f) in sorted(g())][:STOP_AFTER]


def merge_to_binary():
    with open(constants.CORPUS_INDEX, 'w') as fp:
        merge(constants.CORPUS, sorted_files(), fp)


if __name__ == '__main__':
    pass
    # master_merge()

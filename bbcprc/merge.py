"""
Merges many .WAV files into one great big one and keeps track of the sample
offset for each one.
"""

import sys, yaml
from . import files
STOP_AFTER = 10


def merge(directory, outfile, nframes=0, delete_on_fail=False):
    def records(out):
        for i, f in enumerate(files.wave_files(directory)):
            if STOP_AFTER and i >= STOP_AFTER:
                break
            yield f.name, out.tell()
            out.writeframes(files.read_frames(f))
        yield '(END)', out.tell()

    with files.wave_writer(outfile, nframes, delete_on_fail) as out:
        yaml.safe_dump_all(records(out), file=sys.stdout)

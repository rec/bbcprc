from . import audio_io
from . import constants
from . import files
from scipy import signal
import json
import numpy as np
import os

ERROR = 'fp.getframerate() != constants.FRAME_RATE: 48000'


def get_framerate_error_files():
    for f in sorted(files.with_suffix(constants.METADATA_DIR, '.json')):
        if json.load(open(f)).get('error') == ERROR:
            yield constants.source(os.path.basename(f)[:-5])


def resample_file(filename):
    if True:
        original = filename
        filename = filename + '.48KHz'
    else:
        original = filename + '.48KHz'
        os.rename(filename, original)
    fp, frames = audio_io.read_frames_and_fp(original)
    assert fp.getframerate() == 48000
    samples = audio_io.from_frames(frames, fp.getnchannels())
    resampled = np.stack([signal.resample_poly(s, 160, 147) for s in samples])
    audio_io.write(filename, resampled)
    print('Resampled to', filename)


if __name__ == '__main__':
    # resample_file(list(get_framerate_error_files())[
    for f in get_framerate_error_files():
        print(f)

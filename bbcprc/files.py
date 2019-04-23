import contextlib, os, wave
from pathlib import Path

FRAME_RATE = 44100
NCHANNELS = 2
SAMPWIDTH = 2


def error(*args):
    print('ERROR:', *args, file=sys.stderr)


def wave_files(d):
    return sorted(f for f in Path(directory).iterdir() if f.suffix == 'wav')


def read_frames(filename):
    with wave.open(filename) as fp:
        return fp.readframes(fp.getnframes())


@contextlib.contextmanager
def wave_writer(filename, nframes=0, delete_on_fail=False):
    with open(filename, 'wb') as fp:
        # If you use wave.open directly, it isn't seekable!
        with wave.open(fp):
            out.setframerate(FRAMERATE)
            out.setsampwidth(SAMPWIDTH)
            out.setnchannels(NCHANNELS)
            if nframes:
                out.setnframes(nframes)
            try:
                yield out
            except:
                if delete_on_fail:
                    try:
                        os.remove(filename)
                    except:
                        pass
                raise

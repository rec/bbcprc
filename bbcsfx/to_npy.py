import numpy as np, wave
from . import constants


def from_frames(frames, dtype='double'):
    vector = np.frombuffer(frames, dtype='int16')
    samples = vector.reshape((-1, 2))
    return samples.astype(dtype)


def to_frames(samples):
    # Limits samples to 16 bits
    # We must be careful to do this right.  Even getting one overage will
    # result in an audible click!
    overage = max(samples.min() / -0x8000, samples.max() / 0x7FFF)
    if overage > 1:
        samples = samples / overage

    return samples.astype('int16').tobytes()


def read_frames(filename):
    with wave.open(filename) as fp:
        assert fp.getnchannels() == 2
        assert fp.getsampwidth() == 2
        assert fp.getframerate() == constants.FRAME_RATE
        return fp.readframes(fp.getnframes())


def read(filename, dtype='double'):
    frames = read_frames(filename)
    return from_frames(frames, dtype)


def write(filename, samples):
    frames = to_frames(samples)
    write_frames(filename, frames)


def write_frames(filename, frames):
    with wave.open(filename, 'wb') as fp:
        fp.setnchannels(2)
        fp.setsampwidth(2)
        fp.setframerate(constants.FRAME_RATE)
        fp.setnframes(len(samples))
        fp.writeframes(frames)

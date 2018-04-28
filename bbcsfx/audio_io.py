import os, numpy as np, wave
from . import constants, files


def from_frames(frames, nchannels=2, dtype='double'):
    extra = len(frames) % (nchannels * 2)
    if extra:
        frames = frames[:-extra]
    vector = np.frombuffer(frames, dtype='int16')
    samples = vector.reshape((-1, nchannels))
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
    fp, frames = read_frames_and_fp(filename)

    if fp.getnchannels() > 2:
        raise ValueError('fp.getnchannels() > 2')
    if fp.getframerate() != constants.FRAME_RATE:
        raise ValueError('fp.getframerate() != constants.FRAME_RATE: %s'
                         % fp.getframerate())
    return frames, fp.getnchannels()


def read_frames_and_fp(filename):
    with wave.open(filename) as fp:
        if fp.getsampwidth() != 2:
            raise ValueError('fp.getsampwidth() != 2')
        return fp, fp.readframes(fp.getnframes())


def read(filename, dtype='double'):
    frames, nchannels = read_frames(filename)
    return from_frames(frames, nchannels, dtype)


def write(filename, samples):
    frames = to_frames(samples)
    write_frames(filename, frames)


def write_frames(filename, frames):
    assert len(frames) % 4 == 0
    with files.delete_on_fail(filename, wave.open, 'wb') as fp:
        fp.setnchannels(2)
        fp.setsampwidth(2)
        fp.setframerate(constants.FRAME_RATE)
        fp.writeframes(frames)

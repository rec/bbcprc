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


def read(filename, dtype='double'):
    with wave.open(filename) as fp:
        assert fp.getnchannels() == 2
        assert fp.getsampwidth() == 2
        assert fp.getframerate() == constants.FRAME_RATE
        return from_frames(fp.readframes(fp.getnframes()), dtype)


def write(filename, samples):
    with wave.open(filename, 'wb') as fp:
        fp.setnchannels(2)
        fp.setsampwidth(2)
        fp.setframerate(constants.FRAME_RATE)
        fp.setnframes(len(samples))
        fp.writeframes(to_frames(samples))

import wave, numpy as np
from numpy.lib.format import open_memmap

DTYPES = {1: 'int8', 2: 'int16', 3: 'int8', 4: 'int32'}
PARAMS = {'nchannels': 2,
          'sampwidth': 2,
          'framerate': 44100,
          'nframes': 0,
          'comptype': 'NONE',
          'compname': 'not compressed'}


def _shape(p):
    return p.nframes, p.nchannels * (3 if p.sampwidth == 3 else 1)


def reader(filename):
    with open(filename, 'rb') as raw_fp:
        with wave.open(raw_fp) as fp:
            params = fp.getparams()
            offset = raw_fp.tell()
    dtype = DTYPES[params.sampwidth]
    shape = _shape(params)
    return np.memmap(
        filename, mode='r', dtype=dtype, offset=offset, shape=shape)


def writer(filename, nframes, dtype='int16', **params):
    """DEPRECATED"""
    with open(filename, mode='wb') as fp0:
        with wave.open(filename) as fp:
            params = dict(PARAMS, nframes=nframes, **params)
            max_size = 0x100000000 / params['nchannels'] / params['sampwidth']
            params['nframes'] = min(params['nframes'], int(max_size) - 1)
            wp = wave._wave_params(**params)
            fp.setparams(wp)
            shape = _shape(fp.getparams())
            offset = fp0.tell()

    return np.memmap(filename, dtype=dtype, offset=offset, shape=shape)


def memmap(filename, nframes=0, mode='r+', dtype='int16', shape=None):
    # DEPRECATED
    shape = shape or (nframes, 2)
    return open_memmap(filename, mode=mode, dtype=dtype, shape=shape)

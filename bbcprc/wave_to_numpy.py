import wave, numpy as np

DTYPES = {1: 'int8', 2: 'int16', 3: 'int8', 4: 'int32'}
OFFSET = 44
PARAMS = {'nchannels': 2,
          'sampwidth': 2,
          'framerate': 44100,
          'nframes': 0,
          'comptype': 'NONE',
          'compname': 'not compressed'}


def _get_shape(p):
    return p.nframes, p.nchannels * (3 if p.sampwidth == 3 else 1)


def reader(filename):
    with wave.open(filename) as fp:
        params = fp.getparams()
    shape = _get_shape(params)
    dtype = DTYPES[params.sampwidth]
    return np.memmap(filename, dtype=dtype, offset=OFFSET, shape=shape)


def writer(filename, nframes, dtype='int16', **params):
    with wave.open(filename, mode='wb') as fp:
        wp = wave._wave_params(**dict(PARAMS, nframes=nframes, **params))
        fp.setparams(wp)
        shape = _get_shape(fp.getparams())

    return np.memmap(filename, dtype=dtype, offset=OFFSET, shape=shape)

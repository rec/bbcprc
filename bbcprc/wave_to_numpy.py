import wave, numpy as np

DTYPES = {1: 'int8', 2: 'int16', 3: 'int8', 4: 'int32'}
OFFSET = 44
PARAMS = {'nchannels': 2,
          'sampwidth': 2,
          'framerate': 44100,
          'nframes': 0,
          'comptype': 'NONE',
          'compname': 'not compressed'}


def get_shape(p):
    return p.nframes, p.nchannels * (3 if p.sampwidth == 3 else 1)


def reader(filename):
    with open(filename, 'rb') as fp:
        with wave.open(fp) as fp2:
            params = fp2.getparams()
            # offset = fp.tell()
            # assert offset == OFFSET, f'{offset} != {OFFSET}'
            shape = get_shape(params)
            dtype = DTYPES[params.sampwidth]

    return np.memmap(filename, dtype=dtype, offset=OFFSET, shape=shape), params


def writer(filename, nframes, dtype='int16', **params):
    with open(filename, 'wb') as fp:
        with wave.open(fp, mode='wb') as fp2:
            wp = wave._wave_params(**dict(PARAMS, nframes=nframes, **params))
            fp2.setparams(wp)
            shape = get_shape(fp2.getparams())

    return np.memmap(filename, dtype=dtype, offset=OFFSET, shape=shape)

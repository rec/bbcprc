import wave
from wave import Error, Wave_write
from chunk import Chunk

"""A WAV reader that keeps track of chunks"""


class Wave_read(wave.Wave_read):
    def __init__(self, *args, **kwds):
        self.other_chunks = []
        super().__init__(*args, **kwds)

    def initfp(self, file):
        self._convert = None
        self._soundpos = 0
        self._file = Chunk(file, bigendian=0)
        if self._file.getname() != b'RIFF':
            raise Error('file does not start with RIFF id')
        if self._file.read(4) != b'WAVE':
            raise Error('not a WAVE file')
        self._fmt_chunk_read = 0
        self._data_chunk = None
        while 1:
            self._data_seek_needed = 1
            try:
                chunk = Chunk(self._file, bigendian=0)
            except EOFError:
                break
            chunkname = chunk.getname()
            if chunkname == b'fmt ':
                self._read_fmt_chunk(chunk)
                self._fmt_chunk_read = 1
            elif chunkname == b'data':
                if not self._fmt_chunk_read:
                    raise Error('data chunk before fmt chunk')
                self._data_chunk = chunk
                self._nframes = chunk.chunksize // self._framesize
                self._data_seek_needed = 0
                break
            else:
                self.other_chunks.append(chunk.read())
            chunk.skip()
        if not self._fmt_chunk_read or not self._data_chunk:
            raise Error('fmt chunk and/or data chunk missing')


def open(f, mode=None):
    if mode is None:
        if hasattr(f, 'mode'):
            mode = f.mode
        else:
            mode = 'rb'
    if mode in ('r', 'rb'):
        return Wave_read(f)
    elif mode in ('w', 'wb'):
        return Wave_write(f)
    else:
        raise Error("mode must be 'r', 'rb', 'w', or 'wb'")

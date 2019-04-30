# import pathlib, tempfile, unittest, wave
# from bbcprc import wave_to_numpy
import unittest, wave


def to_sample(lo, hi):
    f = 0x100 * hi + lo
    return f if f < 0x8000 else f - 0x10000


def read_frames(filename, nframes):
    with wave.open(filename) as fp:
        frames = []
        for i in range(nframes):
            frame = fp.readframes(1)
            if len(frame) == 2:
                f1 = f2 = frame
            else:
                f1, f2 = frame[:2], frame[2:]
            frames.append([to_sample(*f1), to_sample(*f2)])

        return fp.getparams(), frames


class WaveToNumpyTest(unittest.TestCase):
    def test_mono(self):
        pass
        # reader = wave_to_numpy.reader(MONO_FILE)
        # params, frames = read_frames(MONO_FILE)
        # with wave.open(MONO_FILE) as fp:
        #     params = fp.getparams()
        #     self.assertEqual(reader.shape, (params.nframes, 1))
        #     self.assertEqual(params.nchannels, 1)
        #     frame = list(fp.readframes(1))
        #     sample = list(reader[0])
        #     self.assertEqual(, frame)

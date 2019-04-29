import os, tempfile, unittest
import numpy.testing
from bbcprc import files, merge

F1 = 'f1.wav'
F2 = 'f2.wav'
MMAP = 'mmap.npy'
INDEX = 'mmap.npy.yml'


class MergeTest(unittest.TestCase):
    def test_merge(self):
        with tempfile.TemporaryDirectory() as td:
            os.chdir(td)
            with files.wave_writer(F1, nchannels=1) as fp:
                fp.writeframes(bytes(range(6)))
                self.assertEqual(fp.getnframes(), 3)

            with files.wave_writer(F2, nchannels=2) as fp:
                fp.writeframes(bytes(range(32, 72, 2)))
                self.assertEqual(fp.getnframes(), 5)

            writer = merge.merge(MMAP, 8, (F1, F2), [3, 8])
            expected = [
                [0x100, 0x100], [0x302, 0x302], [0x504, 0x504],

                [0x2220, 0x2624], [0x2a28, 0x2e2c], [0x3230, 0x3634],
                [0x3a38, 0x3e3c], [0x4240, 0x4644]]

            numpy.testing.assert_array_equal(expected, writer)

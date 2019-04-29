import random, unittest, wave
from bbcprc.data import Data
from . import skip_tests
FILE_COUNT = 5


class DataTest(unittest.TestCase):
    def assert_file(self, i):
        samples = Data.samples_at(i)
        with wave.open(Data.names[i]) as fp:
            self.assertEqual(fp.getnframes(), len(samples))
            j = random.randrange(len(samples))
            left, right = samples[j]
            lhi, llo, rhi, rlo = divmod(left, 0x100) + divmod(right, 0x100)

            fp.setpos(j)
            frame = fp.readframes(1)
            if fp.getnchannels() == 1:
                frame += frame
            self.assertEqual(list(frame), [llo, lhi, rlo, rhi])

    @skip_tests.no_source
    @skip_tests.no_corpus
    def test_files(self):
        for i in random.sample(range(len(Data.names)), FILE_COUNT):
            self.assert_file(i)

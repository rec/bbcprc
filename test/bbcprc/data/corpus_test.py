import random, unittest, wave
from bbcprc.data import Corpus
from .. import skip_tests
FILE_COUNT = 5


def _get_wave_frames(fp, index, nframes):
    fp.setpos(index)
    frame = fp.readframes(nframes)
    return list((frame + frame) if fp.getnchannels() == 1 else frame)


def _samples_to_byte_list(sample):
    left, right = ((i if i >= 0 else 0x10000 + i) for i in sample)
    lhi, llo, rhi, rlo = divmod(left, 0x100) + divmod(right, 0x100)
    return [llo, lhi, rlo, rhi]


class CorpusTest(unittest.TestCase):
    @skip_tests.no_source
    @skip_tests.no_corpus
    def test_first(self):
        with wave.open(Corpus.filenames[0]) as fp:
            frame = _get_wave_frames(fp, 0, 1)
        sample = _samples_to_byte_list(Corpus.samples[0][0])
        self.assertEqual(frame, sample)

    @skip_tests.no_source
    @skip_tests.no_corpus
    def test_files(self):
        for i in random.sample(range(len(Corpus.filenames)), FILE_COUNT):
            self.assert_file(i)

    def assert_file(self, i):
        samples = Corpus.samples[i]
        with wave.open(Corpus.filenames[i]) as fp:
            self.assertEqual(fp.getnframes(), len(samples))
            j = random.randrange(len(samples))
            frame = _get_wave_frames(fp, j, 1)
            self.assertEqual(frame, _samples_to_byte_list(samples[j]))

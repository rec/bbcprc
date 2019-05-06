from bbcprc import data
import tempfile
import unittest


class DataTest(unittest.TestCase):
    def _create(self, td):
        return data.WRITE.foo.bar(shape=(300, 2), dtype='int16', root=td)

    def test_read(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                data.READ.foo.bar(root=td)

            self._create(td)[10] = [10, 10]

            bar = data.READ.foo.bar(root=td)
            self.assertEqual(list(bar[10]), [10, 10])
            self.assertEqual(bar.shape, (300, 2))
            with self.assertRaises(ValueError):
                bar[10] = [20, 20]

    def test_readwrite(self):
        with tempfile.TemporaryDirectory() as td:
            self._create(td)[10] = [10, 10]

            bar = data.READWRITE.foo.bar(root=td)
            self.assertEqual(list(bar[10]), [10, 10])
            self.assertEqual(bar.shape, (300, 2))
            bar[10] = [20, 20]

            bar = data.READ.foo.bar(root=td)
            self.assertEqual(list(bar[10]), [20, 20])

    def test_copyonwrite(self):
        with tempfile.TemporaryDirectory() as td:
            self._create(td)[10] = [10, 10]

            bar = data.COPYONWRITE.foo.bar(root=td)
            self.assertEqual(list(bar[10]), [10, 10])
            self.assertEqual(bar.shape, (300, 2))
            bar[10] = [20, 20]

            bar = data.READ.foo.bar(root=td)
            self.assertEqual(list(bar[10]), [10, 10])

    def test_errors(self):
        for maker in data.READ, data.READWRITE, data.COPYONWRITE:
            with tempfile.TemporaryDirectory() as td:
                with self.assertRaises(FileNotFoundError):
                    maker.foo.bar(root=td)

        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                data.WRITE.foo.bar(root=td)

        with tempfile.TemporaryDirectory() as td:
            self._create(td)
            data.READ.foo.bar(root=td)
            with self.assertRaises(ValueError):
                data.READ.foo.bar(shape=(300, 2), dtype='int16', root=td)

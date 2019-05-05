from bbcprc.data import ADDRESS
import tempfile
import unittest


class DataTest(unittest.TestCase):
    def _create(self, td):
        return ADDRESS.foo.bar(
            'w+', shape=(300, 2), dtype='int16', root=td).data

    def test_read(self):
        with tempfile.TemporaryDirectory() as td:
            bar = ADDRESS.foo.bar(root=td)
            with self.assertRaises(FileNotFoundError):
                bar.data

            self._create(td)[10] = [10, 10]

            bar = ADDRESS.foo.bar(root=td)
            self.assertEqual(list(bar.data[10]), [10, 10])
            self.assertEqual(bar.data.shape, (300, 2))
            with self.assertRaises(ValueError):
                bar.data[10] = [20, 20]

    def test_readwrite(self):
        with tempfile.TemporaryDirectory() as td:
            self._create(td)[10] = [10, 10]

            bar = ADDRESS.foo.bar('r+', root=td)
            self.assertEqual(list(bar.data[10]), [10, 10])
            self.assertEqual(bar.data.shape, (300, 2))
            bar.data[10] = [20, 20]

            bar = ADDRESS.foo.bar(root=td)
            self.assertEqual(list(bar.data[10]), [20, 20])

    def test_copyonwrite(self):
        with tempfile.TemporaryDirectory() as td:
            self._create(td)[10] = [10, 10]

            bar = ADDRESS.foo.bar('c', root=td)
            self.assertEqual(list(bar.data[10]), [10, 10])
            self.assertEqual(bar.data.shape, (300, 2))
            bar.data[10] = [20, 20]

            bar = ADDRESS.foo.bar(root=td)
            self.assertEqual(list(bar.data[10]), [10, 10])

    def test_errors(self):
        for mode in 'c', 'r', 'r+':
            with tempfile.TemporaryDirectory() as td:
                data = ADDRESS.foo.bar(mode, root=td)
                with self.assertRaises(FileNotFoundError):
                    data.data

        with tempfile.TemporaryDirectory() as td:
            data = ADDRESS.foo.bar('w+', root=td)
            with self.assertRaises(ValueError):
                data.data

        with tempfile.TemporaryDirectory() as td:
            self._create(td)
            ADDRESS.foo.bar(root=td).data
            data = ADDRESS.foo.bar(shape=(300, 2), dtype='int16', root=td)
            with self.assertRaises(ValueError):
                data.data

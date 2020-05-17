from .save_test import Parent
from bbcprc.util.saver import Saver
import tempfile
import unittest


class SaverTest(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.NamedTemporaryFile() as tf:
            saver = Saver(tf.name, Parent())
            with saver as data:
                self.assertFalse(saver.loaded)
                data.foo = 'bar'
                data.child.bar = 'baz'
                data.child.child.baz = 'bottom'

            saver = Saver(tf.name, Parent())
            with saver as data:
                self.assertTrue(saver.loaded)
                self.assertEqual(data.foo, 'bar')
                self.assertEqual(data.child.bar, 'baz')
                self.assertEqual(data.child.child.baz, 'bottom')

    def test_read_only(self):
        with tempfile.NamedTemporaryFile() as tf:
            saver = Saver(tf.name, Parent(), read_only=True)
            with self.assertRaises(ValueError):
                with saver as data:
                    data.foo = 'bar'
                    got_here = True

            self.assertTrue(got_here)

    def test_no_save(self):
        with tempfile.NamedTemporaryFile() as tf:
            saver = Saver(tf.name, Parent(), must_write=False)
            with saver as data:
                self.assertFalse(saver.loaded)
                data.foo = 'bar'
                data.child.bar = 'baz'
                data.child.child.baz = 'bottom'

            saver = Saver(tf.name, Parent(), must_write=False)
            with saver as data:
                self.assertFalse(saver.loaded)
                self.assertEqual(data.foo, '')
                self.assertEqual(data.child.bar, '')
                self.assertEqual(data.child.child.baz, '')

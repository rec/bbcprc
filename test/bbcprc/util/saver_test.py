import tempfile
import unittest
from bbcprc.util.saver import Saver
from . save_test import Parent


class SaverTest(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.NamedTemporaryFile() as tf:
            parent = Parent()
            with Saver(tf.name, parent) as saver:
                self.assertFalse(saver.loaded)
                parent.foo = 'bar'
                parent.child.bar = 'baz'
                parent.child.child.baz = 'bottom'

            parent = Parent()
            with Saver(tf.name, parent) as saver:
                self.assertTrue(saver.loaded)
                self.assertEqual(parent.foo, 'bar')
                self.assertEqual(parent.child.bar, 'baz')
                self.assertEqual(parent.child.child.baz, 'bottom')

    def test_immutable(self):
        with tempfile.NamedTemporaryFile() as tf:
            parent = Parent()
            with self.assertRaises(ValueError):
                with Saver(tf.name, parent, mutable=False):
                    parent.foo = 'bar'
                    got_here = True

            self.assertTrue(got_here)

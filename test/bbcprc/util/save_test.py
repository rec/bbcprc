import unittest
from attr import dataclass, Factory
from bbcprc.util.save import save, load


class SaveTest(unittest.TestCase):
    def test_round_trip(self):
        c = Child()
        c.bar = 'bar'
        c.child.baz = 'baz'

        ser = save(c)
        d = load(ser, Child())
        self.assertEqual(c, d)

    def test_round_trip2(self):
        p1 = Parent()
        p1.foo = 'foo'
        p1.child.bar = 'bar'
        p1.child.child.baz = 'baz'

        ser = save(p1)
        p2 = load(ser, Parent())
        self.assertEqual(p1, p2)

    def test_round_trip_fail(self):
        p1 = Parent()
        p1.foo = 'foo'
        p1.child.bar = 'bar'
        p1.child.child.baz = 1  # wrong type!

        ser = save(p1)
        p2 = load(ser, Parent())
        self.assertNotEqual(p1, p2)


@dataclass
class Grandchild:
    baz: str = ''


@dataclass
class Child:
    bar: str = ''
    child: Grandchild = Factory(Grandchild)


@dataclass
class Parent:
    foo: str = ''
    child: Child = Factory(Child)

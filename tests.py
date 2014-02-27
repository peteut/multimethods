import unittest
from multimethods import (MultiMethod, Default, type_dispatch, DispatchException, Anything,
                          singledispatch, multidispatch, multimethod)

identity = lambda x: x


class Basic(unittest.TestCase):
    def test_basics(self):
        speaksum = MultiMethod('speaksum', lambda *a: sum(a))

        @speaksum.method(2)
        def _speaksum2(x, y, z):
            return "Two"

        @speaksum.method(5)
        def _speaksum5(x, y):
            return "Five"

        @speaksum.method(Default)
        def _speaksum_d(x, y, z):
            return "Another"

        self.assertEqual(speaksum(1, 1, 0), "Two")
        self.assertEqual(speaksum(3, 2), "Five")
        self.assertEqual(speaksum(9, 8, 2), "Another")
        self.assertEqual(speaksum(3, 5, 6), "Another")

        # Too many arguments to method
        self.assertRaises(TypeError, lambda: speaksum(2, 3, 0, 0, 0))

    def test_addmethod(self):
        foomethod = MultiMethod('foomethod', identity)

        foomethod.addmethod(lambda x: "The Answer", 42)
        foomethod.addmethod(lambda x: "2^10", 1024)
        foomethod.addmethod(lambda x: "Nothing", Default)

        self.assertEqual(foomethod(42), "The Answer")
        self.assertEqual(foomethod(1024), "2^10")
        self.assertEqual(foomethod(Default), "Nothing")

    def test_removemethod(self):
        barmethod = MultiMethod('barmethod', identity)

        @barmethod.method(1)
        def barmethod1(x):
            return 123

        self.assertEqual(barmethod(1), 123)

        barmethod.removemethod(1)
        self.assertRaises(Exception, lambda: barmethod(1))

        @barmethod.method(Default)
        def barmethod_d(x):
            return 42

        self.assertEqual(barmethod("whatever"), 42)
        self.assertEqual(barmethod("something"), 42)

        barmethod.removemethod(Default)
        self.assertRaises(Exception, lambda: barmethod("whatever"))
        self.assertRaises(Exception, lambda: barmethod(1))

    def test_name_conflict(self):
        # Shouldn't cause any problems
        foobar1 = MultiMethod('foobar', identity)
        foobar2 = MultiMethod('foobar', identity)

        @foobar1.method(1)
        def foobar1(x):
            return "foobar1"

        @foobar2.method(2)
        def foobar2(selfx):
            return "foobar2"

        self.assertEqual(foobar1(1), "foobar1")
        self.assertEqual(foobar2(2), "foobar2")


class Item(object):
    pass


class BoxedItem(Item):
    pass


class FragileItem(BoxedItem):
    pass


class ExpensiveItem(Item):
    pass


class Dispatch(unittest.TestCase):

    discount = MultiMethod('tests.Dispatch.discount', lambda name, item: (len(name), type(item)))

    @discount.method((5, ExpensiveItem))
    def dis_25(name, item):
        return 25

    @discount.method((10, ExpensiveItem))
    def dis_30(name, item):
        return 30

    @discount.method((Anything, ExpensiveItem))
    def dis_15(name, item):
        return 15

    @discount.method((5, Item))
    def dis_5(name, item):
        return 5

    discount.prefer((Anything, ExpensiveItem), (5, Item))

    @discount.method(Default)
    def default(name, item):
        return 0

    def test_hierarchy(self):
        self.assertEqual(self.discount("steve", ExpensiveItem()), 25)
        self.assertEqual(self.discount("chrisjones", ExpensiveItem()), 30)
        self.assertEqual(self.discount("steve", BoxedItem()), 5)
        self.assertEqual(self.discount("joe", Item()), 0)

    def test_anything(self):
        self.assertEqual(self.discount("joe", ExpensiveItem()), 15)


class Prefer(unittest.TestCase):

    bar = MultiMethod('bar', type_dispatch)

    @bar.method((object, str))
    def barstr(x, y):
        return "os " + str(x) + y

    @bar.method((str, object))
    def barsrto(x, y):
        return "so " + x + str(y)

    @bar.method(Default)
    def bardef(x, y):
        return "default"

    barpref = MultiMethod('barpref', type_dispatch)

    @barpref.method((object, str))
    def barstrp(x, y):
        return "os " + str(x) + y

    @barpref.method((str, object))
    def barsrtop(x, y):
        return "so " + x + str(y)

    @barpref.method(Default)
    def bardefp(x, y):
        return "default"

    barpref.prefer((str, object), (object, str))

    def test_ambiguous(self):
        self.assertEqual(self.bar(5, 6), "default")
        self.assertRaises(DispatchException, self.bar, "sdf", "dgf")

    def test_prefer(self):
        self.assertEqual(self.barpref(5, 6), "default")
        self.assertEqual(self.barpref("sdf", "dgf"), "so sdfdgf")

    def test_prefer_not_needed_on_same_method(self):
        bar = MultiMethod('bar', type_dispatch)

        @bar.method((object, str))
        @bar.method((str, object))
        def barstr(x, y):
            return "os " + str(x) + str(y)

        @bar.method((int, int))
        def other(x, y):
            return 5

        self.assertEqual(bar("sdf", "dgf"), "os sdfdgf")
        self.assertEqual(bar(3, 6), 5)
    
def mylen(x):
    return len(x)


class Decorators(unittest.TestCase):

    @multimethod(mylen)
    def mm(x):
        return "default"

    def test_multimethod(self):
        self.assertEqual(self.mm.methods[Default].__name__, "mm")
        self.assertEqual(self.mm.dispatchfn, mylen)
        self.assertEqual(self.mm.__name__, "tests.mm")

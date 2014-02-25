<<<<<<< HEAD
# -*- encoding: utf-8 -*-

from nose.tools import assert_equal, assert_raises
from multimethodic import MultiMethod, Default

identity = lambda x: x


def test_basics():
    speaksum = MultiMethod('speaksum', lambda *a: sum(a))

    @speaksum.method(2)
    def speaksum(x, y, z):
        return "Two"

    @speaksum.method(5)
    def speaksum(x, y):
        return "Five"

    @speaksum.method(Default)
    def speaksum(x, y, z):
        return "Another"

    assert_equal(speaksum(1, 1, 0), "Two")
    assert_equal(speaksum(3, 2), "Five")
    assert_equal(speaksum(9, 8, 2), "Another")
    assert_equal(speaksum(3, 5, 6), "Another")

    # Too many arguments to method
    assert_raises(TypeError, lambda: speaksum(2, 3, 0, 0, 0))


def test_addmethod():
    foomethod = MultiMethod('foomethod', identity)

    foomethod.addmethod(lambda x: "The Answer", 42)
    foomethod.addmethod(lambda x: "2^10", 1024)
    foomethod.addmethod(lambda x: "Nothing", Default)

    assert_equal(foomethod(42), "The Answer")
    assert_equal(foomethod(1024), "2^10")
    assert_equal(foomethod(Default), "Nothing")


def test_removemethod():
    barmethod = MultiMethod('barmethod', identity)

    @barmethod.method(1)
    def barmethod(x):
        return 123

    assert_equal(barmethod(1), 123)

    barmethod.removemethod(1)
    assert_raises(Exception, lambda: barmethod(1))

    @barmethod.method(Default)
    def barmethod(x):
        return 42

    assert_equal(barmethod("whatever"), 42)
    assert_equal(barmethod("something"), 42)

    barmethod.removemethod(Default)
    assert_raises(Exception, lambda: barmethod("whatever"))
    assert_raises(Exception, lambda: barmethod(1))


def test_name_conflict():
    # Shouldn't cause any problems
    foobar1 = MultiMethod('foobar', identity)
    foobar2 = MultiMethod('foobar', identity)

    @foobar1.method(1)
    def foobar1(x):
        return "foobar1"

    @foobar2.method(2)
    def foobar2(x):
        return "foobar2"

    assert_equal(foobar1(1), "foobar1")
    assert_equal(foobar2(2), "foobar2")


if __name__ == '__main__':
    import nose
    nose.runmodule()
=======
import unittest

from multimethods import MultiMethod, method


class NamespaceTests(unittest.TestCase):
    def test_definition_ns_required(self):
        self.assertRaises(TypeError, MultiMethod, 'definition', lambda value: value)

    def test_decorator_ns_required(self):
        MultiMethod('decorator', lambda value: value, ns='custom')

        try:
            @method(1)
            def decorator(value):
                pass
        except TypeError:
            pass
        else:
            self.fail('method decorator does not require namespace')

    def test_definition(self):
        MultiMethod('definition', lambda value: value, ns='custom')
        assert MultiMethod.instances.get('custom.definition'), "namespace is not 'custom'"

    def test_installed_methods(self):
        MultiMethod('installing', lambda value: value, ns='custom')

        try:
            @method(1, ns='custom')
            def installing(value):
                pass
        except KeyError:
            self.fail('not installing multimethods within namespace')
>>>>>>> refs/remotes/exupero/master

import unittest

from multimethods import MultiMethod, method


class NamespaceTests(unittest.TestCase):
    def test_definition(self):
        MultiMethod('definition', lambda value: value)
        assert MultiMethod.instances.get('tests.definition'), "namespace is not 'tests'"

    def test_installed_methods(self):
        MultiMethod('installing', lambda value: value)

        try:
            @method(1)
            def installing(value):
                pass
        except KeyError:
            self.fail('not installing multimethods within namespace')

    def test_overriding(self):
        MultiMethod('overriding', lambda value: value, ns='overridden')
        assert MultiMethod.instances.get('overridden.overriding'), 'namespace cannot be overridden'

    def test_overriding_installed(self):
        MultiMethod('installed.overriding', lambda value: value)

        try:
            @method(1)
            def installing(value):
                pass
        except KeyError:
            self.fail('namespace cannot be overridden for methods')

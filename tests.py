import unittest

from multimethods import MultiMethod, method


class NamespaceTests(unittest.TestCase):
    def test_definition(self):
        mm = MultiMethod('definition', lambda value: value)
        assert MultiMethod.instances.get('tests.definition'), "namespace is not 'tests'"

    def test_installed_methods(self):
        MultiMethod('installing', lambda value: value)

        try:
            @method(1)
            def installing(value):
                pass
        except KeyError:
            self.fail('not installing multimethods within namespace')

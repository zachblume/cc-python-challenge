from unittest import TestCase

from src.domain.model import Model


class TestModel(TestCase):

    def test_is_global_for_commodity__commodity_matches_and_scope_none__returns_true(self):
        model = Model('Copper', None, 12.34)

        self.assertTrue(
            model.is_global_for_commodity('Copper'),
            'Model should be global because is matches commodity and has None scope')

    def test_is_global_for_commodity__commodity_matches_but_scope_not_none__returns_false(self):
        model = Model('Copper', 'India', 12.34)

        self.assertFalse(
            model.is_global_for_commodity('Copper'),
            'Model should not be global because it has non-None scope')

    def test_is_global_for_commodity__scope_is_none_but_commodity_does_not_match__returns_false(self):
        model = Model('Copper', None, 12.34)

        self.assertFalse(
            model.is_global_for_commodity('Zinc'),
            'Model should not be global for the commodity because the commodity does not match')

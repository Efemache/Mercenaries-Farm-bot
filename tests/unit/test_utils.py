import unittest

from modules.utils import update


class TestUtils(unittest.TestCase):
    def test_update_empty_base(self):
        base_dictionary = {}
        updated_dictionary = {
            "a": 1,
            "b": 2,
        }

        expected_dictionary = {
            "a": 1,
            "b": 2,
        }
        actual_dictionary = update(base_dictionary, updated_dictionary)

        assert expected_dictionary == actual_dictionary

    def test_update(self):
        base_dictionary = {
            "a": 0,
            "b": 0,
            "c": 3,
        }
        updated_dictionary = {
            "a": 1,
            "b": 2,
        }

        expected_dictionary = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        actual_dictionary = update(base_dictionary, updated_dictionary)

        assert expected_dictionary == actual_dictionary

    def test_update_empty_update(self):
        base_dictionary = {
            "a": 1,
            "b": 2,
        }
        updated_dictionary = {}

        expected_dictionary = {
            "a": 1,
            "b": 2,
        }
        actual_dictionary = update(base_dictionary, updated_dictionary)

        assert expected_dictionary == actual_dictionary

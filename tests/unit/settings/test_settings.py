import unittest
from unittest.mock import patch
from pathlib import Path

from modules.settings.conf.settings import (
    get_settings,
    copy_config_from_sample_if_not_exists,
)
from modules.exceptions import UnsetGameDirectory, MissingGameDirectory


class TestSettings(unittest.TestCase):
    @patch("pathlib.Path.is_dir")
    def test_get_settings(self, mock_is_dir):
        test_settings_filename = "tests/unit/settings/test_settings.ini"
        mock_is_dir.return_value = True
        actual_settings_dict = get_settings(test_settings_filename)

        expected_settings_dict = {
            "bot_speed": 0.1,
            "gamedir": "C:/Test/Location/Hearthstone",
            "level": 5,
            "location": "The Barrens",
            "mode": "Heroic",
            "monitor": 1,
            "monitor resolution": "1920x1080",
            "mousespeed": 0.3,
            "quitbeforebossfight": False,
            "stopatstranger": False,
            "waitforexp": 0,
            "zonelog": "C:/Test/Location/Hearthstone/Logs/Zone.log",
            "notificationurl": "https://example.com",
        }

        self.assertEqual(actual_settings_dict, expected_settings_dict)

    def test_get_settings_no_gamedir(self):
        self._extracted_from_test_get_settings_missing_gamedir_2(
            "tests/unit/settings/test_settings_no_gamedir.ini",
            UnsetGameDirectory,
            "Game Dir setting is not set",
        )

    def test_get_settings_missing_gamedir(self):
        """
        Test to check if correct exception is raised
        if gamedir doesn't exist in filesystem
        """
        self._extracted_from_test_get_settings_missing_gamedir_2(
            "tests/unit/settings/test_settings_missing_gamedir.ini",
            MissingGameDirectory,
            "Game directory (c:\\location\\that\\doesnt\\exist) does not exist",
        )

    # TODO Rename this here and in `test_get_settings_no_gamedir` and `test_get_settings_missing_gamedir`
    def _extracted_from_test_get_settings_missing_gamedir_2(self, arg0, arg1, arg2):
        test_settings_filename = arg0
        with self.assertRaises(arg1) as context:
            get_settings(test_settings_filename)
        self.assertEqual(arg2, str(context.exception))

    @patch("pathlib.Path.is_file")
    def test_copy_config_from_sample_if_not_exists(self, mock_is_file):
        """
        Test copy config function if file exists
        """
        mock_is_file.return_value = True

        copy_config_from_sample_if_not_exists("filename.txt")

        mock_is_file.assert_called_once_with()

    @patch("shutil.copy")
    @patch("pathlib.Path.is_file")
    def test_copy_config_from_sample_if_not_exists_when_no_config(
        self, mock_is_file, mock_copy
    ):
        """
        Test copy config function when file doesn't exist
        """
        mock_is_file.side_effect = [False, True]

        copy_config_from_sample_if_not_exists("filename.txt")

        mock_copy.assert_called_once_with(
            Path("filename.txt.sample"), Path("filename.txt")
        )

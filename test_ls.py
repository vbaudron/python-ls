import os
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

from ls import parse_arguments, LISTING_ARG, DirectoryListingPrinter


class ParserTest(unittest.TestCase):

    def test_parser(self):
        valid_path = os.getcwd()

        # SIMPLE : Valid Directory
        sys_args = [valid_path]
        args = parse_arguments(args=sys_args)
        self.assertEqual(args.path, valid_path)
        self.assertFalse(args.show_details)

        # OPTION : Valid Directory + -l
        sys_args = [valid_path, LISTING_ARG]
        args = parse_arguments(args=sys_args)
        self.assertEqual(args.path, valid_path)
        self.assertTrue(args.show_details)

        # ERROR : No Arg
        sys_args = list()
        with self.assertRaises(SystemExit) as se_mock:
            parse_arguments(args=sys_args)
            self.assertEqual(se_mock.exception.code, 2)

        # ERROR : Too Many Args
        sys_args = [valid_path, "another_arg"]
        with self.assertRaises(SystemExit) as se_mock:
            parse_arguments(args=sys_args)
            self.assertEqual(se_mock.exception.code, 2)


class DirectoryListingPrinterTest(unittest.TestCase):

    def test_init(self):
        valid_path = os.getcwd()
        invalid_add = "invalid"
        invalid_path = valid_path + os.path.sep + invalid_add
        details = True

        # Valid Path + Default details
        listing = DirectoryListingPrinter(path=valid_path)
        self.assertEqual(listing.path, valid_path)
        self.assertEqual(listing.display_details, False)
        self.assertEqual(listing.prefix, None)

        # Valid Path + specified details
        listing = DirectoryListingPrinter(path=valid_path, details=details)
        self.assertEqual(listing.path, valid_path)
        self.assertEqual(listing.display_details, details)
        self.assertEqual(listing.prefix, None)

        # Prefix - path does not exist
        self.assertFalse(os.path.exists(invalid_path))
        listing = DirectoryListingPrinter(path=invalid_path)
        self.assertEqual(listing.path, valid_path)
        self.assertEqual(listing.display_details, False)
        self.assertEqual(listing.prefix, invalid_add)

        # Prefix - path is File
        filename = "ls.py"
        file_path = valid_path + os.path.sep + filename
        self.assertTrue(os.path.exists(file_path) and os.path.isfile(file_path))
        listing = DirectoryListingPrinter(path=file_path)
        self.assertEqual(listing.path, valid_path)
        self.assertEqual(listing.display_details, False)
        self.assertEqual(listing.prefix, filename)

    def test_start(self):
        valid_path = os.getcwd()
        prefix = "prefix"
        invalid_path = valid_path + "not_valid_anymore"
        full_path = invalid_path + os.path.sep + prefix

        # -- Non Valid Path --
        listing = DirectoryListingPrinter(path=full_path)
        self.assertEqual(listing.path, invalid_path)
        self.assertEqual(listing.display_details, False)
        self.assertEqual(listing.prefix, prefix)
        with patch('logging.error') as mock:
            listing.start()
            mock.assert_called_with("Directory path is NOT valid", exc_info=True)

        # -- START --

        # Mock creation for File To KEEP - Valid file
        file_in_entries_mock = MagicMock(is_file=True)
        file_in_entries_mock_name = PropertyMock(return_value='file')
        type(file_in_entries_mock).name = file_in_entries_mock_name

        # -- Not A File --

        # listing creation
        listing = DirectoryListingPrinter(path=valid_path)

        # Mock creation for NOT to keep - Not a file
        not_in_entries_mock = MagicMock(is_file=False)
        not_in_entries_mock_name = PropertyMock(return_value='not_a_file')
        type(not_in_entries_mock).name = not_in_entries_mock_name

        scan_return = [file_in_entries_mock, not_in_entries_mock]
        with patch('os.scandir', return_value=scan_return) as patched_scan:
            listing.start()
            patched_scan.assert_called_with(path=valid_path)
            self.assertNotIn(not_in_entries_mock, listing.entries_to_print)
            self.assertIn(file_in_entries_mock, listing.entries_to_print)

        # -- Hidden File --

        # listing creation
        listing = DirectoryListingPrinter(path=valid_path)

        # Mock creation for NOT to keep - hidden file
        not_in_entries_mock = MagicMock(is_file=False)
        not_in_entries_mock_name = PropertyMock(return_value='.hidden_file')
        type(not_in_entries_mock).name = not_in_entries_mock_name

        scan_return = [file_in_entries_mock, not_in_entries_mock]
        with patch('os.scandir', return_value=scan_return) as patched_scan:
            listing.start()
            patched_scan.assert_called_with(path=valid_path)
            self.assertNotIn(not_in_entries_mock, listing.entries_to_print)
            self.assertIn(file_in_entries_mock, listing.entries_to_print)

        # -- Prefix --
        # listing creation
        prefix = "prefix"
        path = valid_path + os.path.sep + prefix
        listing = DirectoryListingPrinter(path=path)

        # Mock creation for File To KEEP - Valid file
        file_in_entries_mock = MagicMock(is_file=True)
        file_in_entries_mock_name = PropertyMock(return_value=prefix + '_file')
        type(file_in_entries_mock).name = file_in_entries_mock_name

        # Mock creation for NOT to keep - No Prefix
        not_in_entries_mock = MagicMock(is_file=True)
        not_in_entries_mock_name = PropertyMock(return_value='without_prefix_file')
        type(not_in_entries_mock).name = not_in_entries_mock_name

        scan_return = [file_in_entries_mock, not_in_entries_mock]
        with patch('os.scandir', return_value=scan_return) as patched_scan:
            listing.start()
            patched_scan.assert_called_with(path=valid_path)
            self.assertNotIn(not_in_entries_mock, listing.entries_to_print)
            self.assertIn(file_in_entries_mock, listing.entries_to_print)

    def test_print_entries(self):
        valid_path = os.getcwd()

        mode = {
            "st_mode": 33261,
            "str_mode": "-rwxr-xr-x"
        }
        date = {
            "st_birthtime": 1579122563.2759194,
            "str_datetime": "2020-01-15 22:09"
        }

        # -- No Details Printing --
        listing = DirectoryListingPrinter(path=valid_path)
        self.assertEqual(listing.path, valid_path)
        self.assertEqual(listing.display_details, False)
        self.assertEqual(listing.prefix, None)

        # Mock File
        stat_mock = MagicMock(
            st_mode=mode["st_mode"],
            st_birthtime=date["st_birthtime"]
        )
        config_mock = {
            'stat.return_value': stat_mock
        }
        file_mock = MagicMock(is_file=True, **config_mock)
        file_mock_name = PropertyMock(return_value='file_1')
        type(file_mock).name = file_mock_name

        scan_return = [file_mock]
        with patch('os.scandir', return_value=scan_return):
            with patch('builtins.print') as print_patched:
                listing.start()
                print_patched.assert_called_with(file_mock.name)

        # -- Details Printing --
        listing = DirectoryListingPrinter(path=valid_path, details=True)
        self.assertEqual(listing.path, valid_path)
        self.assertEqual(listing.display_details, True)
        self.assertEqual(listing.prefix, None)

        # Mock File
        stat_mock = MagicMock(
            st_mode=mode["st_mode"],
            st_birthtime=date["st_birthtime"]
        )
        config_mock = {
            'stat.return_value': stat_mock
        }
        file_mock = MagicMock(is_file=True, **config_mock)
        file_mock_name = PropertyMock(return_value='file_1')
        type(file_mock).name = file_mock_name

        scan_return = [file_mock]
        with patch('os.scandir', return_value=scan_return):
            with patch('builtins.print') as print_patched:
                listing.start()
                print_patched.assert_called_with(
                    mode["str_mode"],
                    ' ',
                    date["str_datetime"],
                    file_mock.name
                )


if __name__ == '__main__':
    unittest.main()

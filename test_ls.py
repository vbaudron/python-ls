import os
import unittest

from ls import parse_arguments, LISTING_ARG, DirectoryListingPrinter


class ParserTestCase(unittest.TestCase):

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
            args = parse_arguments(args=sys_args)
            self.assertEqual(se_mock.exception.code, 2)

        # ERROR : Too Many Args
        sys_args = [valid_path, "another_arg"]
        with self.assertRaises(SystemExit) as se_mock:
            args = parse_arguments(args=sys_args)
            self.assertEqual(se_mock.exception.code, 2)


class DirectoryListingPrinterTestCase(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()

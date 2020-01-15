import os
import unittest

from ls import parse_arguments, LISTING_ARG


class LsTestCase(unittest.TestCase):

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



if __name__ == '__main__':
    unittest.main()

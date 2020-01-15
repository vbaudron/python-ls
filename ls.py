#! /usr/bin/env python3
# coding: utf-8

from argparse import ArgumentParser


LISTING_ARG = "-l"


def parse_arguments(args=None):
    parser = ArgumentParser(description="A simplified ls - list directory contents")

    # Arguments to Parse
    parser.add_argument("path", help="file path to list")
    parser.add_argument(LISTING_ARG, help="display mode & creation date", action="store_true", dest="show_details")

    return parser.parse_args(args=args)


def main():
    args = parse_arguments()


if __name__ == "__main__":
    main()

#! /usr/bin/env python3
# coding: utf-8
import os
from argparse import ArgumentParser
import logging as log


LISTING_ARG = "-l"


# ===============
# LS class
# ===============

class DirectoryListingPrinter:
    __path: str
    __display_details: bool
    __prefix: str

    def __init__(self, path: str, details=False):
        self.__path = path
        self.__display_details = details

        # handle Prefix
        if not os.path.exists(self.__path) or os.path.isfile(self.__path):
            self.__handle_prefix()
        else:
            self.__prefix = None

    def __handle_prefix(self):
        # Split path with pertinent separator
        split = self.__path.split(os.path.sep)

        # Extract Prefix - the last one
        idx_last = len(split) - 1
        self.__prefix = split[idx_last]

        # Remove Prefix from path
        split.pop(idx_last)
        self.__path = os.path.sep.join(split)

    def __str__(self) -> str:
        return """[ListingPrinter] path : '{}' - display_details : {} - prefix : {}""".format(
            self.__path,
            self.__display_details,
            "'{}'".format(self.__prefix) if self.__prefix else None
        )

    # ----------
    # Properties
    # ----------
    @property
    def path(self):
        return self.__path

    @property
    def display_details(self):
        return self.__display_details

    @property
    def prefix(self):
        return self.__prefix


# ======================
# Arguments Check Method
# ======================

def parse_arguments(args=None):
    parser = ArgumentParser(description="A simplified ls - list directory contents")

    # Arguments to Parse
    parser.add_argument("path", help="file path to list")
    parser.add_argument(LISTING_ARG, help="display mode & creation date", action="store_true", dest="show_details")

    return parser.parse_args(args=args)


# ===========
# Main Method
# ===========

def main():
    # Parse Arguments
    args = parse_arguments()
    log.debug("args parsed : " + args.__str__())

    # Process Listing
    listing = DirectoryListingPrinter(path=args.path, details=args.show_details)
    log.debug(listing)


if __name__ == "__main__":
    main()

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
    __entries_to_print: list

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

    def start(self):
        self.__entries_to_print = list()
        try:
            for entry in os.scandir(path=self.__path):
                # only file AND not hidden ones AND which satisfies prefix if require
                if self.__is_file_not_hidden(entry=entry) and self.__satisfy_prefix_requirement(entry_name=entry.name):
                    self.__entries_to_print.append(entry)

        except (NotADirectoryError, FileNotFoundError):
            log.error("Directory path is NOT valid", exc_info=True)

    def __is_file_not_hidden(self, entry: os.DirEntry) -> bool:
        return entry.is_file and not entry.name.startswith('.')

    def __satisfy_prefix_requirement(self, entry_name: str) -> bool:
        return not self.__prefix or entry_name.startswith(self.__prefix)

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

    @property
    def entries_to_print(self):
        return self.__entries_to_print




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
    listing.start()


if __name__ == "__main__":
    main()

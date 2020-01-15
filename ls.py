#! /usr/bin/env python3
# coding: utf-8
import datetime
import logging as log
import os
import stat
from argparse import ArgumentParser

LISTING_ARG = "-l"
TIME_FORMAT = '%Y-%m-%d %H:%M'


# ===============
# LS class
# ===============

class DirectoryListingPrinter:
    """Class use to print not hidden file name from a directory path.
    optional details can be also printed.

    # -----
    # INIT
    # -----
    instance created from :

    - Path Directory to list files in it
    - Optional details is true to print more file details

    If the path does not exist, the last part of path will be considered as a 'prefix' and will be required to choose
    which files to print

    ex :
    FOLDER : '/path/to/folder/'
    CONTAINS Files :
        some_file
        another_file

    CASE 1 : path = '/path/to/folder/' ==> path exists
    prefix = None
    --> files to print :
        some_file
        another_file

    CASE 2 : path = '/path/to/folder/som' ==> path does not exist
    prefix = 'som'
    path = '/path/to/folder/'
    --> files to print :
        some_file

    # -----
    # START
    # -----
    method used to select files from folder and print them.

    SELECT :
    - Only file
    - Not hidden
    - with the prefix required if so

    PRINT :
    - file name
    if details attribute is True add :
        - mode
        - creation datetime

    ex : (see folder upper)

    CASE 3 : path = '/path/to/folder/som'  details = True
    prefix = 'som'
    path = '/path/to/folder/'
    display_details = true
    --> files to print :
        rwxr--r--  2017-12-15 17:44 some_file

    """

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

    # --------------
    # PUBLIC Method
    # --------------

    def start(self):
        self.__entries_to_print = list()
        try:
            for entry in os.scandir(path=self.__path):
                # only file AND not hidden ones AND which satisfy prefix if require
                if self.__is_file_not_hidden(entry=entry) and self.__satisfy_prefix_requirement(entry_name=entry.name):
                    self.__entries_to_print.append(entry)

        except (NotADirectoryError, FileNotFoundError):
            log.error("Directory path is NOT valid", exc_info=True)

        self.__print_entries()

    # ---------------
    # Handle Prefix
    # ---------------

    def __handle_prefix(self):
        # Split path with pertinent separator
        split = self.__path.split(os.path.sep)

        # Extract Prefix - the last one
        idx_last = len(split) - 1
        self.__prefix = split[idx_last]

        # Remove Prefix from path
        split.pop(idx_last)
        self.__path = os.path.sep.join(split)

    # ---------------------
    # Select Files to print
    # ---------------------

    def __is_file_not_hidden(self, entry: os.DirEntry) -> bool:
        return entry.is_file and not entry.name.startswith('.')

    def __satisfy_prefix_requirement(self, entry_name: str) -> bool:
        return not self.__prefix or entry_name.startswith(self.__prefix)

    # -----------
    # Print Files
    # -----------

    def __print_entries(self):
        if self.__display_details:
            for entry in self.__entries_to_print:
                dir_entry: os.DirEntry = entry
                entry_stat = dir_entry.stat()
                str_mode = stat.filemode(entry_stat.st_mode)
                creation_time = datetime.datetime.fromtimestamp(entry_stat.st_birthtime)
                print(str_mode, ' ', creation_time.strftime(TIME_FORMAT), entry.name)
        else:
            for entry in self.__entries_to_print:
                print(entry.name)

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

    def __str__(self) -> str:
        return """[ListingPrinter] path : '{}' - display_details : {} - prefix : {}""".format(
            self.__path,
            self.__display_details,
            "'{}'".format(self.__prefix) if self.__prefix else None
        )


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

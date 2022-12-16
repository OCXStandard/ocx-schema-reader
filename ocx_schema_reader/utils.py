#  Copyright (c) 3-2022 OCX Consortium (https://3docx.org). See the LICENSE.

import errno
import logging
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict

import yaml

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))


def nested_dict():
    """
    Creates a default dictionary where each value is an other default dictionary.
    """
    return defaultdict(nested_dict)


def default_to_regular(d) -> Dict:
    """
    Converts defaultdicts of defaultdicts to dict of dicts.

    Args:
        d: The dict to be converted

    """
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def default_to_grid(d) -> Dict:
    """
    Converts defaultdicts to a data grid with unique row ids.

    Args:
        d: The dict to be converted

    """
    if isinstance(d, defaultdict):
        print(d.items())
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def get_path_dict(paths):
    new_path_dict = nested_dict()
    for path in paths:
        parts = path.split("/")
        if parts:
            marcher = new_path_dict
            for key in parts[:-1]:
                marcher = marcher[key]
            marcher[parts[-1]] = parts[-1]
    return default_to_regular(new_path_dict)


# Components for pretty print a directory tree structure
# prefix components:
space = "    "
branch = "│   "
# pointers:
tee = "├── "
last = "└── "


def tree(paths: dict, prefix: str = ""):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(paths) - 1) + [last]
    for pointer, path in zip(pointers, paths):
        yield prefix + pointer + path
        if isinstance(paths[path], dict):  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(paths[path], prefix=prefix + extension)


def number_table_rows(table: dict, first_index: int = 0) -> Dict:
    """Utility function to add row numbers to the first column of a table stored as a dict

    Args:
        table. The input table dict

    Returns:
        a table (dict) with numbered rows in the first column

    """
    size = len(list(table.values())[0])
    tbl = defaultdict(list)
    for i in range(first_index, size + first_index):
        tbl["#"].append(i)
    tbl.update(table)  # Join the columns
    return tbl


def find_replace_multi(string, dictionary) -> str:
    for item in dictionary.keys():
        # sub item for item's paired value in string
        string = re.sub(item, dictionary[item], string)
    return string


def logging_level(loglevel: str) -> int:
    """Utility function to return the logging level
    Args:
        loglevel (str) One of 'INFO, 'WARNING', 'ERROR' or 'DEBUG
    Return:
        level (int) The Python logging level
    """
    # Set the console logging level
    level = logging.INFO
    if loglevel == "ERROR":
        level = logging.ERROR
    elif loglevel == "WARNING":
        level = logging.WARNING
    elif loglevel == "DEBUG":
        level = logging.DEBUG
    return level


def list_files_in_directory(directory: str, file_ext: str = ".3docx") -> list:
    """Utility function to list files in a directory.

    aRGS:
        directory: the name of the directory.
        file_ext: Only files with matching extension will be listed.
    Returns:
       list of matching files.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise AssertionError(errno.EEXIST)
    file_list = []
    for x in sorted(dir_path.iterdir()):
        if x.is_file() and x.suffix.lower() == file_ext:
            file_list.append(x.name)
    return file_list


def load_yaml_config(config: Path) -> dict:
    """Safely read a yaml config file and return the content as a dict"""
    if config.exists():
        with open(config.absolute()) as f:
            app_config = yaml.safe_load(f)
        return app_config
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config.absolute())

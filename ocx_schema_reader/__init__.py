#  Copyright (c) 3-2022. OCX Consortium https://3docx.org. See the LICENSE

import logging
from pathlib import Path

import click_log

from ocx_schema_reader.utils import ROOT_DIR, load_yaml_config

"""Expose package-wide elements."""

__version__ = "0.1.0.dev1"

""" Examples of valid version strings according :pep:`440#version-scheme`:
.. code-block:: python
    __version__ = '1.2.3.dev1'   # Development release 1
    __version__ = '1.2.3a1'      # Alpha Release 1
    __version__ = '1.2.3b1'      # Beta Release 1
    __version__ = '1.2.3rc1'     # RC Release 1
    __version__ = '1.2.3'        # Final Release
    __version__ = '1.2.3.post1'  # Post Release 1
"""
MODULE_CONFIG = Path(ROOT_DIR) / "ocx_schema_reader" / "config.yaml"
config = load_yaml_config(MODULE_CONFIG)

INFO_COLOR = config.get("INFO_COLOR")
ERROR_COLOR = config.get("ERROR_COLOR")
APP = config.get("APP")
DEFAULT_SCHEMA = config.get("DEFAULT_SCHEMA")
SCHEMA_FOLDER = config.get("SCHEMA_FOLDER")

logger = logging.getLogger(__name__)
click_log.basic_config(logger)

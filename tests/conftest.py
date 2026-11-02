#  Copyright (c) 2022. OCX Consortium https://3docx.org. See the LICENSE

import logging
import os
import sys

import pytest

# To make sure that the tests import the ocx_schema_reader modules this has to come before the import statements
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ocx_tools.schema.parser import OcxSchema
from ocx_tools.schema_xml.parse import LxmlParser

logger = logging.Logger(__name__)


@pytest.fixture
def load_schema_from_file(shared_datadir) -> LxmlParser:
    parser = LxmlParser(logger)
    test_data = shared_datadir / "OCX_Schema.xsd"
    parser.parse(test_data)
    assert parser.lxml_version() == (4, 9, 2, 0)
    return parser


@pytest.fixture
def process_schema(shared_datadir, load_schema_from_file) -> OcxSchema:
    test_data = shared_datadir / "OCX_Schema.xsd"
    url = str(test_data.resolve())
    schema_folder = shared_datadir
    folder = str(schema_folder.resolve())
    schema_reader = OcxSchema(logger, folder)
    result = schema_reader.process_schema(url)
    assert result is True
    return schema_reader

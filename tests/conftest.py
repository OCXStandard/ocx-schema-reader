import logging

import pytest

from ocx_schema_reader.schema_reader import OcxSchema
from ocx_xml.xml_parser import LxmlParser

logger = logging.getLogger(__name__)


@pytest.fixture
def load_schema(shared_datadir) -> LxmlParser:
    parser = LxmlParser(logger)
    test_data = shared_datadir / "OCX_Schema.xsd"
    parser.parse(test_data)
    assert parser.lxml_version() == (4, 9, 1, 0)
    return parser


@pytest.fixture
def process_schema(shared_datadir, load_schema: LxmlParser) -> OcxSchema:
    test_data = shared_datadir / "OCX_Schema.xsd"
    url = str(test_data.resolve())
    schema_folder = shared_datadir
    folder = str(schema_folder.resolve())
    schema_reader = OcxSchema(logger, folder)
    result = schema_reader.process_schema(url)
    assert result is True
    return schema_reader

import logging
import unittest
from pathlib import Path
from unittest import TestCase

import yaml

from ocx_schema_reader.schema_reader import OcxSchema
from ocx_schema_reader.utils import ROOT_DIR

config = Path(ROOT_DIR) / "ocx_schema_reader" / "config.yaml"
MODULE_CONFIG = config.absolute()

with open(MODULE_CONFIG) as f:
    app_config = yaml.safe_load(f)

DEFAULT_SCHEMA = app_config.get("DEFAULT_SCHEMA")
SCHEMA_FOLDER = app_config.get("SCHEMA_FOLDER")

logger = logging.getLogger()
schema_reader = OcxSchema(logger, SCHEMA_FOLDER)


class TestOcxSchema(TestCase):
    def test_process_schema(self, schema=DEFAULT_SCHEMA):
        result = schema_reader._parse_schema(schema)
        self.assertTrue(result)

    def test_schema_version(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        version = schema_reader.get_schema_version()
        self.assertEqual(version, "2.8.7")

    def test_get_schema_folder(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        schema_folder = schema_reader.get_schema_folder()
        self.assertEqual(schema_folder, SCHEMA_FOLDER)

    def test_get_default_schema(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        default_schema = schema_reader.get_default_schema()
        self.assertEqual(default_schema, DEFAULT_SCHEMA)

    def test_is_parsed(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        self.assertTrue(schema_reader.is_parsed())

    def test_get_all_schema_elements(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_all_schema_elements()
        self.assertEqual(len(result), 637)

    def test_get_ocx_elements(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader.get_ocx_elements()
        self.assertEqual(len(result), 327)

    def test_get_ocx_element_from_type(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        vessel = schema_reader.get_ocx_element_from_type("ocx:Vessel")
        self.assertEqual(vessel.get_name(), "Vessel")

    def test_schema_changes(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        # Filter out only '2.8.6' changes
        result = [v for v in schema_reader.get_schema_changes()["Version"] if "2.8.6" in v]
        self.assertEqual(len(result), 29)

    def test_get_schema_complex_types(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_schema_complex_types()
        self.assertEqual(len(result), 189)

    def test_get_schema_simple_types(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_schema_simple_types()
        self.assertListEqual(
            result,
            [
                "{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}booleanListType",
                "{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}classificationSociety",
                "{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}curveForm_enum",
                "{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}doubleListType",
                "{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}floatListType",
                "{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}guid",
                "{https://3docx.org/fileadmin//ocx_schema//V287//OCX_Schema.xsd}integerListType",
            ],
        )

    def test_get_schema_attributes(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_schema_attributes()
        self.assertEqual(len(result), 121)

    def test_get_schema_attribute_groups(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader._get_schema_attribute_groups()
        self.assertEqual(len(result), 11)

    def test_summary_table(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        summary = schema_reader.tbl_summary()
        self.maxDiff = None
        self.assertListEqual(
            summary["Item"],
            [
                "Schema Version",
                "Number of element types",
                "Number of attribute types",
                "Number of complexType types",
                "Number of simpleType types",
                "Number of attributeGroup types",
                "Number of namespaces",
                "xml",
                "xs",
                "vc",
                "xlink",
                "ocx",
                "unitsml",
                None,
                "xsd",
            ],
        )

    def test_tbl_attribute_groups(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader.tbl_attribute_groups()
        self.assertEqual(len(result), 5)

    def test_tbl_simple_types(self):
        if not schema_reader.is_parsed():
            schema_reader.process_schema(DEFAULT_SCHEMA)
        result = schema_reader.tbl_simple_types()
        self.assertEqual(len(result), 5)


if __name__ == "__main__":
    unittest.main()

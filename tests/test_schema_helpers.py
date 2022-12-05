from ocx_schema_reader.schema_helpers import SchemaHelper
from ocx_xml.xml_parser import LxmlParser


class TestSchemaHelpers:
    def test_get_schema_version(self, data_regression, load_schema: LxmlParser):
        """Test retrieving the OCX schema version

        Args:
            data_regression: pytest regression test framework
            load_schema: Shared test data provided by @pytest.fixture in ``conftest.py``
        """
        root = load_schema.get_root()
        version = SchemaHelper.get_schema_version(root)
        assert version == "2.8.7"

    def test_find_schema_changes(self, data_regression, load_schema: LxmlParser):
        """Test retrieving the OCX schema changes

        Args:
            data_regression: pytest regression test framework
            load_schema: Shared test data provided by @pytest.fixture in ``conftest.py``
        """
        root = load_schema.get_root()
        data = SchemaHelper.schema_changes_data_grid(root)
        data_regression.check(data)

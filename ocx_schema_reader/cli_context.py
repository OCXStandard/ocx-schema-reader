#  Copyright (c) 2022.  OCX Consortium https://3docx.org. See the LICENSE

from collections import defaultdict
from typing import Any, DefaultDict, Dict


class GlobalContext:
    """Class holding global context information to be shared between subcommands

    Attributes:
        _tools: Pointers to toolset that can be shared
        _table_format: The formatting used when outputting tables. Default=`outline`
        _table_output: Output tables to a file or `stdout` (default)
    """

    def __init__(self):
        self._tools: Dict[Any] = {}
        self._table_format: str = "simple"
        self._table_output: str = "stdout"
        self._table_column_separator: str = "U+0020"  # Whitespace

    def register_tool(self, tool: Any):
        """Register a tool with the global context"""
        self._tools[tool.__name__] = tool

    def get_tool(self, name: str) -> Any:
        """Return the toll with name `name`"""
        return self._tools.get(name)

    def table_format(self, fmt: str = "simple"):
        """Set the table formatter option
        Args:
            fmt: set output table format; supported formats:
                      plain, simple, github, grid, fancy_grid, pipe,
                      orgtbl, rst, mediawiki, html, latex, latex_raw,
                      latex_booktabs, latex_longtable, tsv
                      (default: simple)
        """
        self._table_format = fmt

    def table_output(self, file: str = "stdout"):
        """Print tables to a file.

        Args:
            file: The file name for table output. Subsequent table output will be amended to the end of the file.
                    Default = `stdout`

        """
        self._table_output = file

    def table_column_separator(self, sep: str = "U+0020"):
        """Set the table column character separator.

        Args:
            sep: The column separator character  for tables. Default = whitespace

        """
        self._table_column_separator = sep

    def get_column_separator(self) -> str:
        """Get the table column character separator.

        Returns:
            sep: The table column separator character for tables

        """
        return self._table_column_separator

    def get_table_output(self) -> str:
        """Get the table output destination.

        Returns:
            file: The file name for table output. Subsequent table output will be amended to the end of the file.
                    Default = `stdout`

        """
        return self._table_output

    def get_table_format(self) -> str:
        """Get the table formatter option

        Returns:
            fmt: The output table format

        """
        return self._table_format

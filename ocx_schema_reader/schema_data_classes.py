from dataclasses import dataclass, field, fields
from typing import Dict, List, Tuple


@dataclass
class BaseDataClass:
    """Base class for OCX dataclasses.
    Each sub-class has to implement a field metadata with nam e``header`` for each of its attributes, for example:
    ```name : str = field(metadata={'header': '<User friendly field name>'})```
    """

    def to_dict(self) -> Dict:
        """Output the data class as a dict with field names as keys"""
        my_fields = fields(self)
        table = {}
        i = 0
        for key, value in self.__dict__.items():
            table[my_fields[i].metadata["header"]] = value
            i += 1
        return table


@dataclass
class SchemaChange(BaseDataClass):
    """Class for keeping track of OCX schema changes

    Args:
         version: The schema version the change applies to
         author: The author of the schem change
         date: The date of the schema change
         description: A description of the change

    """

    version: str = field(metadata={"header": "Version"})
    author: str = field(metadata={"header": "Author"})
    date: str = field(metadata={"header": "Date"})
    description: str = field(default="", metadata={"header": "Description"})


@dataclass
class SchemaType(BaseDataClass):
    """Class for xsd schema type information

    Args:
         name: The schema type name
         prefix: The schema type namespace prefix
         source_line: The line number in the schema file where the type is defined
         tag: The schema type tag

    """

    prefix: str = field(metadata={"header": "Prefix"})
    name: str = field(metadata={"header": "Name"})
    tag: str = field(metadata={"header": "Tag"})
    source_line: int = field(metadata={"header": "Source Line"})


@dataclass
class SchemaSummary(BaseDataClass):
    """Class for schema summary information

    Args:
         schema_version: The schema version
         schema_types: Tuples of the number of schema types
         schema_namespaces: schema namespaces

    """

    schema_version: str = field(metadata={"header": "Schema Version"})
    schema_types: List[Tuple] = field(metadata={"header": "Schema Types"})
    schema_namespaces: List[Tuple] = field(metadata={"header": "Namespaces"})
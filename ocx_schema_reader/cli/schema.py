#  Copyright (c) 3-2023.  OCX Consortium https://3docx.org. See the LICENSE

from collections import defaultdict

from click_shell import shell
from click import Choice, prompt
from click import Path as ClickPath
from click import argument, option, pass_context, secho
from fuzzywuzzy import fuzz
from tabulate import tabulate
from ocx_schema_reader.schema_xml.element import LxmlElement
from ocx_schema_reader.parse.reader import OcxSchema
from .cli_context import GlobalContext

import ocx_schema_reader.utils as utils
from .config import INFO_COLOR, ERROR_COLOR, APP
from ocx_schema_reader.parse.config import DEFAULT_SCHEMA, SCHEMA_FOLDER

PROMPT = "SCHEMA"


def print_table(table: list, glob_ctx: GlobalContext, to_list: bool = True):
    fmt = glob_ctx.get_table_format()
    # sep = glob_ctx.get_column_separator()
    # out = glob_ctx.get_table_output()
    index_rows = glob_ctx.get_row_numbers()
    if to_list:
        result = utils.dict_to_list(table, index_rows)
        secho(tabulate(result, headers="firstrow", tablefmt=fmt), fg=INFO_COLOR)
    else:
        secho(tabulate(table, headers="firstrow", tablefmt=fmt, showindex=index_rows), fg=INFO_COLOR)


@shell(prompt=f"{PROMPT} > ", intro=f"Starting {PROMPT}..")
@pass_context
def schema(ctx):
    """The schema subcommands"""
    pass


@schema.command(short_help="The OCX xsd file to be parsed.")
@pass_context
@option(
    "-s",
    "--schema_file",
    help="Assign an OCX xsd file to be parsed. It must " "be a valid file path.",
    prompt="Assign an OCX xsd file to be parsed",
    type=ClickPath(exists=True),
)
def assign_schema(ctx, schema_file):
    """Assign an OCX xsd file to be parsed using the `parse` subcommand."""
    schema_reader = ctx.obj.get_tool("OcxSchema")
    schema_reader.put_default_schema(schema_file)
    secho(
        f"Assigned new default schema: {schema_reader.get_default_schema()}",
        fg=INFO_COLOR,
    )


@schema.command(help="Assign the default schema folder")
@option(
    "--folder",
    prompt="Directory containing the XSD schema files",
    help="Assign the default schema folder",
    type=ClickPath(exists=True),
)
@pass_context
def assign_folder(ctx, schema_folder):
    """Assign the default folder containing the schema xsd files"""
    schema_reader = ctx.obj.get_tool("OcxSchema")
    schema_reader.put_schema_folder(schema_folder)
    secho(
        f"Assigned new schema folder: {schema_reader.get_schema_folder()}",
        fg=INFO_COLOR,
    )


@schema.command(short_help="Print the schema change history")
@pass_context
@option(
    "-v",
    "--version",
    type=Choice(["All", "Current"], case_sensitive=False),
    prompt="Current or all historic schema version changes",
    default="Current",
    help="Print the list of schema changes for the current version (default) or all historic versions",
)
def changes(ctx, version):
    """Print the list of schema changes for the current version (default) or all historic versions"""
    glob_ctx = ctx.obj
    schema_reader = glob_ctx.get_tool("OcxSchema")
    schema_changes = schema_reader.get_schema_changes()
    if schema_reader.is_parsed():
        table = [["Version", "Author", "Date", "Change"]]
        current_version = schema_reader.get_schema_version()
        for c in schema_changes:
            if version.lower() == "current":
                if c.version == current_version:
                    table.append([c.version, c.author, c.date, c.description])
            else:
                table.append([c.version, c.author, c.date, c.description])
        print_table(table, glob_ctx, False)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="Output a schema summary")
@pass_context
def summary(ctx):
    """Output the schema summary information."""
    glob_ctx = ctx.obj
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        summary = schema_reader.tbl_summary()
        table = [["Item", "Value"]]
        for item in summary.schema_version:
            table.append(item)
        for item in summary.schema_types:
            table.append(item)
        for item in summary.schema_namespaces:
            table.append(item)
        print_table(table, glob_ctx, False)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="Parse the xsd")
@option(
    "--xsd",
    prompt="Name of the schema XSD file to be parsed. It can also be a valid URL:",
    default=DEFAULT_SCHEMA,
    required=False,
)
@pass_context
def parse(ctx, xsd):
    """Parse the schema XSD file"""
    glob_ctx = ctx.obj
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.process_schema(xsd):
        secho(f"The schema {xsd} has been successfully parsed", fg=INFO_COLOR)
    else:
        secho(f"An error occurred when parsing the  {xsd}", fg=ERROR_COLOR)


@schema.command(short_help="List attributeGroup")
@pass_context
def attribute_groups(ctx):
    """Output all elements of type `xs:attributeGroup`"""
    glob_ctx = ctx.obj
    schema_reader = ctx.obj.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        result = schema_reader.tbl_attribute_groups()
        print_table(result, glob_ctx)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="List simpleType")
@pass_context
def simple_types(ctx):
    """Output all the schema elements of type `xs:simpleType`."""
    glob_ctx = ctx.obj
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        result = schema_reader.tbl_simple_types()
        print_table(result, glob_ctx)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="List all attribute elements")
@pass_context
def attributes(ctx):
    """Output all schema elements of type `xs:attribute`."""
    glob_ctx = ctx.obj
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        result = schema_reader.tbl_attribute_types()
        print_table(result, glob_ctx)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="List all complexType elements")
@pass_context
def complex(ctx):
    """Output all schema elements of type `xs:complexType`."""
    glob_ctx = ctx.obj
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        result = schema_reader.tbl_complex_types()
        print_table(result, glob_ctx)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="List all element types")
@pass_context
def element_types(ctx):
    """Output all schema elements of type `xs:element`."""
    glob_ctx = ctx.obj
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        result = schema_reader.tbl_element_types()
        print_table(result, glob_ctx)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="List schema namespaces")
@pass_context
def namespace(ctx):
    """Output all schema namespaces with its associated prefix."""
    glob_ctx = ctx.obj
    fmt = glob_ctx.get_table_format()
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        result = schema_reader.get_namespaces()
        table = defaultdict(list)
        for key, values in result.items():
            table["Prefix"].append(key)
            table["Namespace"].append(values)
        secho(tabulate(table, headers=list(table.keys()), tablefmt=fmt), fg=INFO_COLOR)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="inspect a schema element")
@argument("element", type=str, nargs=1)
@pass_context
def inspect(ctx, element):
    """Inspect a named schema ELEMENT. Enter the named ELEMENT to be inspected "
    including any namespace prefix on the form `prefix:Name`.
    The output includes all attributes and subtypes of the ELEMENT and"
    the ELEMENT super types.
    """
    glob_ctx = ctx.obj
    fmt = glob_ctx.get_table_format()
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        e = schema_reader.get_ocx_element_from_type(element)
        if e is not None:
            secho(
                f"Global element {e.get_name()} of type {e.get_type()}: {e.get_annotation()}",
                fg=INFO_COLOR,
            )
            secho("\nSub-elements:", fg=INFO_COLOR)
            result = e.children_to_dict()
            secho(tabulate(result, headers=list(result.keys()), tablefmt=fmt), fg=INFO_COLOR)
            secho("\nAttributes:", fg=INFO_COLOR)
            result = e.attributes_to_dict()
            secho(tabulate(result, headers=list(result.keys()), tablefmt=fmt), fg=INFO_COLOR)
            items = e.get_parents()
            parents = []
            for key in items:
                parents.append(LxmlElement.strip_namespace_tag(key))
            secho(f"Parents: {parents}", fg=INFO_COLOR)
            secho(f"\nHas assertions: {e.has_assertion()}", fg=INFO_COLOR)
            for test in e.get_assertion_tests():
                secho(f"Test: {test}", fg=INFO_COLOR)
        else:
            secho(
                f"ERROR: The {element} named entity is not defined in the schema",
                fg=ERROR_COLOR,
            )
            global_elements = [
                f"{element.get_prefix()}:{element.get_name()}" for element in schema_reader.get_ocx_elements()
            ]
            closest = max([(fuzz.token_set_ratio(element, j), j) for j in global_elements])
            ans = prompt(f"Did you mean {closest[1]}? (Yes/No)", default="Yes")
            if ans.lower() == "yes" or ans.lower() == "y":
                ctx.invoke(inspect, closest[1])
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="List all schema elements")
@pass_context
def elements(ctx):
    """Output all the global schema elements."""
    glob_ctx = ctx.obj
    fmt = glob_ctx.get_table_format()
    # sep = glob_ctx.get_column_separator()
    # out = glob_ctx.get_table_output()
    index_rows = glob_ctx.get_row_numbers()
    schema_reader = glob_ctx.get_tool("OcxSchema")
    if schema_reader.is_parsed():
        table = defaultdict(list)
        ocx_elements = schema_reader.get_ocx_elements()
        for e in ocx_elements:
            table["Prefix"].append(e.get_prefix())
            table["Name"].append(e.get_name())
            table["Type"].append(e.get_type())
            table["Abstract"].append(e.is_abstract())
            table["SubstitutionGroup"].append(e.get_substitution_group())
            table["Attributes"].append([a.get_name() for a in e.get_attributes()])
            table["Parents"].append(e.get_parent_names())
            table["Description"].append(e.get_annotation())
            table["Namespace"].append(e.get_namespace())
        if index_rows:
            table = number_table_rows(table, 1)
        secho(tabulate(table, headers=list(table.keys()), tablefmt=fmt), fg=INFO_COLOR)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)

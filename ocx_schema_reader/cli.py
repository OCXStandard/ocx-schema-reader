#  Copyright (c) 3-2022. OCX Consortium https://3docx.org. See the LICENSE

import logging
from collections import defaultdict
from pathlib import Path

import numpy as np
from click_shell import shell
from click import Choice, prompt
from click import Path as ClickPath
from click import argument, option, pass_context, secho
from fuzzywuzzy import fuzz
from tabulate import tabulate

from ocx_schema_reader.schema_elements import LxmlElement
from ocx_schema_reader.schema_reader import OcxSchema

from ocx_schema_reader.utils import (dict_to_list, number_table_rows)
from ocx_schema_reader import logger, INFO_COLOR, ERROR_COLOR, APP, DEFAULT_SCHEMA, SCHEMA_FOLDER


schema_reader = OcxSchema(logger, SCHEMA_FOLDER)


@shell(prompt=f"{APP} > ", intro=f"Starting {APP}..")
@pass_context
def schema(ctx):
    """ The schema subcommands"""
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
def \
        assign_folder(schema_folder):
    """Assign default OCX schema"""
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
    """ Print the list of schema changes for the current version (default) or all historic versions"""
    schema_changes = schema_reader.get_schema_changes()
    if version.lower() == "current":
        table = defaultdict(list)
        current_version = schema_reader.get_schema_version()
        arr = np.array(schema_changes["Version"])
        where = np.argwhere(arr == current_version)
        i, k = where[0], where[-1]
        for key, result in schema_changes.items():
            sliced = result[i[0]: k[0]]
            table[key] = sliced
        schema_changes = table
    secho(tabulate(schema_changes, headers=list(schema_changes.keys())), fg=INFO_COLOR)


@schema.command(short_help="Output schema summary")
@pass_context
def summary(ctx):
    """Output the schema summary information."""
    if schema_reader.is_parsed():
        result = schema_reader.tbl_summary()
        # secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)
        secho(tabulate(result), fg=INFO_COLOR)
    else:
        secho("No schema has been parsed. Parse a schema first", fg=INFO_COLOR)


@schema.command(short_help="Parse the xsd")
@option(
    "--schema_file",
    prompt="Name of the schema XSD file",
    default=schema_reader.get_default_schema(),
    type=ClickPath(),
    help="Parse a schema",
)
@pass_context
def parse(ctx, schema_file):
    """Parse the schema XSD file."""
    if schema_reader.process_schema(schema_file):
        secho(f"The schema {schema_file} has been successfully parsed", fg=INFO_COLOR)
    else:
        secho(f"An error occurred when parsing the  {schema_file}", fg=ERROR_COLOR)


@schema.command(short_help="List attributeGroup")
@option("-r", "--row_numbers", flag_value=True, help="Use this flag to turn off row numbers", default=True)
@pass_context
def attribute_groups(ctx, row_numbers):
    """Output all elements of type `xs:attributeGroup`"""
    result = dict_to_list(schema_reader.tbl_attribute_groups(), row_numbers)
    secho(tabulate(result, headers='firstrow'), fg=INFO_COLOR)


@schema.command(short_help="List simpleType")
@option("-r", "--row_numbers", flag_value=True, help="Use this flag to turn off row numbers", default=True)
@pass_context
def simple_types(ctx, row_numbers):
    """Output all the schema elements of type `xs:simpleType`."""
    result = dict_to_list(schema_reader.tbl_simple_types(), row_numbers)
    secho(tabulate(result, headers='firstrow'), fg=INFO_COLOR)


@schema.command(short_help="List all attribute elements")
@option("-r", "--row_numbers", flag_value=True, help="Use this flag to turn off row numbers", default=True)
@pass_context
def attributes(ctx, row_numbers):
    """Output all schema elements of type `xs:attribute`."""
    result = dict_to_list(schema_reader.tbl_attribute_types(), row_numbers)
    secho(tabulate(result, headers='firstrow'), fg=INFO_COLOR)


@schema.command(short_help="List all complexType elements")
@option("-r", "--row_numbers", flag_value=True, help="Use this flag to turn off row numbers", default=True)
@pass_context
def complex(ctx, row_numbers):
    """Output all schema elements of type `xs:complexType`."""
    result = dict_to_list(schema_reader.tbl_complex_types(), row_numbers)
    secho(tabulate(result, headers='firstrow'), fg=INFO_COLOR)


@schema.command(short_help="List all element types")
@option("-r", "--row_numbers", flag_value=True, help="Use this flag to turn off row numbers", default=True)
@pass_context
def element_types(ctx, row_numbers):
    """Output all schema elements of type `xs:element`."""
    result = dict_to_list(schema_reader.tbl_element_types(), row_numbers)
    secho(tabulate(result, headers='firstrow'), fg=INFO_COLOR)


@schema.command(short_help="List schema namespaces")
@pass_context
def namespace(ctx):
    """Output all schema namespaces with its associated prefix."""
    # schema_reader = ctx.obj
    result = schema_reader.get_namespaces()
    table = defaultdict(list)
    for key, values in result.items():
        table["Prefix"].append(key)
        table["Namespace"].append(values)
    secho(tabulate(table, headers=list(table.keys())), fg=INFO_COLOR)


@schema.command(short_help="inspect a schema element")
@argument("element", type=str, nargs=1)
@pass_context
def inspect(ctx, element):
    """Inspect a named schema ELEMENT. Enter the named ELEMENT to be inspected "
    including any namespace prefix on the form `prefix:Name`.
    The output includes all attributes and subtypes of the ELEMENT and"
    the ELEMENT super types.
    """
    e = schema_reader.get_ocx_element_from_type(element)
    if e is not None:
        secho(
            f"Global element {e.get_name()} of type {e.get_type()}: {e.get_annotation()}",
            fg=INFO_COLOR,
        )
        secho("\nSub-elements:", fg=INFO_COLOR)
        result = e.children_to_dict()
        secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)
        secho("\nAttributes:", fg=INFO_COLOR)
        result = e.attributes_to_dict()
        secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)
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
        ans = prompt(f"Did you mean {closest[1]}? (Yes/No)", default='Yes')
        if ans.lower() == "yes" or ans.lower() == 'y':
            ctx.invoke(inspect, closest[1])


@schema.command(short_help="List all schema elements")
@option("-r", "--row_numbers", flag_value=True, help="Use this flag to turn off row numbers", default=True)
def elements(row_numbers):
    """Output all the global schema elements."""

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
    if row_numbers:
        table = number_table_rows(table, 1)
    secho(tabulate(table, headers=list(table.keys())), fg=INFO_COLOR)

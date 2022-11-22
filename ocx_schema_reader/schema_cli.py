#  Copyright (c) 3-2022 OCX Consortium (https://3docx.org). See the LICENSE.
import logging

import numpy as np
from pathlib import Path
import click
from click_shell import shell
from tabulate import tabulate
from collections import defaultdict
from fuzzywuzzy import fuzz
from ocx_schema_reader.utils import load_yaml_config, ROOT_DIR, number_table_rows
from ocx_schema_reader.schema__reader import OcxSchema
from ocx_schema_reader.schema_elements import LxmlElement

MODULE_CONFIG = Path(ROOT_DIR) / 'ocx_schema_reader' / 'config.yaml'
config = load_yaml_config(MODULE_CONFIG)

INFO_COLOR = config.get('INFO_COLOR')
ERROR_COLOR = config.get('ERROR_COLOR')
APP = config.get('APP')
DEFAULT_SCHEMA = config.get('DEFAULT_SCHEMA')
SCHEMA_FOLDER = config.get('SCHEMA_FOLDER')
logger = logging.getLogger()

schema_reader = OcxSchema(logger, SCHEMA_FOLDER)


@shell(prompt=f"{APP} > ", intro=f"{APP} sub-commands")
@click.pass_context
def schema(ctx):
    #ctx.invoke(parse)
    pass


@schema.command(help='Assign the default schema XSD schema file')
@click.pass_context
@click.option(
    "-s",
    "--assign-schema", "schema",
    prompt=True,
    type=click.Path(exists=True)
)
def assign_schema(ctx, schema_file):
    """Assign default OCX schema"""
    schema_reader.put_default_schema(schema_file)
    click.secho(f'Assigned new default schema: {schema_reader.get_default_schema()}', fg=INFO_COLOR)


@schema.command(help='Assign the default schema folder')
@click.pass_context
@click.option(
    "-s",
    "--assign-schema", "schema",
    prompt=True,
    type=click.Path(exists=True)
)
def assign_folder(ctx, schema_folder):
    """Assign default OCX schema"""
    schema_reader.put_schema_folder(schema_folder)
    click.secho(f'Assigned new schema folder: {schema_reader.get_schema_folder()}', fg=INFO_COLOR)


@schema.command(help='Output the schema changes')
@click.pass_context
@click.option(
    "--version",
    type=click.Choice(['All', 'Current'], case_sensitive=False),
    prompt="Current or all historic schema version changes",
    default="Current")
def changes(ctx, version):
    changes = schema_reader.get_schema_changes()
    if version.lower() == 'current':
        table = defaultdict(list)
        current_version = schema_reader.get_schema_version()
        arr = np.array(changes['Version'])
        where = np.argwhere(arr == current_version)
        i, k = where[0], where[-1]
        for key, result in changes.items():
            sliced = result[i[0]:k[0]]
            table[key] = sliced
        changes = table
    click.secho(tabulate(changes, headers=list(changes.keys())), fg=INFO_COLOR)


@schema.command(help='Output the schema summary info')
@click.pass_context
def summary(ctx):
    if schema_reader.is_parsed():
        result = schema_reader.tbl_summary()
        click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)
    else:
        click.secho(f'No schema has been parsed. Parse a schema first', fg=INFO_COLOR)


@schema.command(help='Parse a schema')
@click.option('-schema',
              prompt=True,
              default=schema_reader.get_default_schema(),
              type=click.Path(),
              help="Name of the schema XSD file")
@click.pass_context
def parse(ctx, schema):
    if schema_reader.process_schema(schema):
        click.secho(f'The schema {schema} has been successfully parsed', fg=INFO_COLOR)
        ctx.obj = schema_reader
    else:
        click.secho(f'An error occurred when parsing the  {schema}', fg=ERROR_COLOR)


@schema.command(help='Output all attributeGroup elements')
@click.pass_context
@click.option('--row_numbers', flag_value=True, default=True)
def attribute_groups(ctx, row_numbers):
    result = schema_reader.tbl_attribute_groups()
    if row_numbers:
        result = number_table_rows(result, 1)
    click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)


@schema.command(help='Output the all simpleType elements')
@click.pass_context
@click.option('--row_numbers', flag_value=True, default=True)
def simple_types(ctx, row_numbers):
    result = schema_reader.tbl_simple_types()
    if row_numbers:
        result = number_table_rows(result, 1)
    click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)


@schema.command(help='Output all attribute elements')
@click.pass_context
@click.option('--row_numbers', flag_value=True, default=True)
def attributes(ctx, row_numbers):
    result = schema_reader.tbl_attribute_types()
    if row_numbers:
        result = number_table_rows(result, 1)
    click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)


@schema.command(help='Output the all complexType elements')
@click.pass_context
@click.option('--row_numbers', flag_value=True, default=True)
def complex(ctx, row_numbers):
    result = schema_reader.tbl_complex_types()
    if row_numbers:
        result = number_table_rows(result, 1)
    click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)


@schema.command(help='Output  all elements of type element')
@click.pass_context
@click.option('--row_numbers', flag_value=True, default=True)
def element_types(ctx, row_numbers):
    # schema_reader = ctx.obj
    result = schema_reader.tbl_element_types()
    if row_numbers:
        result = number_table_rows(result, 1)
    click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)


@schema.command(help='Output the parsed schema namespaces')
@click.pass_context
def namespace(ctx):
    # schema_reader = ctx.obj
    result = schema_reader.get_namespaces()
    table = defaultdict(list)
    for key, values in result.items():
        table['Prefix'].append(key)
        table['Namespace'].append(values)
    click.secho(tabulate(table, headers=list(table.keys())), fg=INFO_COLOR)


@schema.command(help='Inspect a named schema element. Enter the named ELEMENT to be inspected '
                     'including any namespace prefix on the form "prefix:Name".'
                     ' The output includes all attributes and sub types of the ELEMENT and'
                     ' the ELEMENT super types.')
@click.pass_context
@click.argument('element', type=str, nargs=1)
def inspect(ctx, element):
    e = schema_reader._get_ocx_element_from_type(element)
    if e is not None:
        click.secho(f'Global element {e.get_name()} of type {e.get_type()}: {e.get_annotation()}', fg=INFO_COLOR)
        click.secho('\nSub-elements:', fg=INFO_COLOR)
        result = e.children_to_dict()
        click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)
        click.secho('\nAttributes:', fg=INFO_COLOR)
        result = e.attributes_to_dict()
        click.secho(tabulate(result, headers=list(result.keys())), fg=INFO_COLOR)
        items = e.get_parents()
        parents = []
        for key in items:
            parents.append(LxmlElement.strip_namespace_tag(key))
        click.secho(f'Parents: {parents}', fg=INFO_COLOR)
        click.secho(f'\nHas assertions: {e.has_assertion()}', fg=INFO_COLOR)
        for test in e.get_assertion_tests():
            click.secho(f'Test: {test}', fg=INFO_COLOR)
    else:
        click.secho(f'ERROR: The {element} is not defined in the schema', fg=ERROR_COLOR)
        global_elements = [f'{element.get_prefix()}:{element.get_name()}' for element in
                           schema_reader.get_ocx_elements()]
        closest = max([(fuzz.token_set_ratio(element, j), j) for j in global_elements])
        click.secho(f'INFO: Did you mean {closest[1]}?', fg=INFO_COLOR)


@schema.command(help='Output the schema global elements')
@click.pass_context
@click.option('--row_numbers', flag_value=True, default=True)
def elements(ctx, row_numbers):
    table = defaultdict(list)
    elements = schema_reader.get_ocx_elements()
    for e in elements:
        table['Prefix'].append(e.get_prefix())
        table['Name'].append(e.get_name())
        table['Type'].append(e.get_type())
        table['Abstract'].append(e.is_abstract())
        table['SubstitutionGroup'].append(e.get_substitution_group())
        table['Attributes'].append([a.get_name() for a in e.get_attributes()])
        table['Parents'].append(e.get_parent_names())
        table['Description'].append(e.get_annotation())
        table['Namespace'].append(e.get_namespace())
    if row_numbers:
        table = number_table_rows(table, 1)
    click.secho(tabulate(table, headers=list(table.keys())), fg=INFO_COLOR)

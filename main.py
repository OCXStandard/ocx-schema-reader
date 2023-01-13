#  Copyright (c) 2022-2023.  OCX Consortium https://3docx.org. See the LICENSE

"""Allow the module to be run as a CLI. I.e.:
.. code-block:: shell-session
    $ python -m meta_package_manager
Removes empty string and current working directory from the first entry of
`sys.path`, if present to avoid using current directory
in subcommands when invoked as `python -m meta_package_manager <command>`.
"""

from ocx_tools.cli.cli_main import cli

if __name__ == "__main__":
    cli()
    # from ocx_schema_reader.cli import schema
    # Execute the CLI but force its name to not let Click defaults to:
    # "python -m ocx_schema_reader".
    # schema(prog_name=schema.name)

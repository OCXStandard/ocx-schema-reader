#  Copyright (c) 2022. OCX Consortium https://3docx.org. See the LICENSE

"""Allow the module to be run as a CLI. I.e.:
.. code-block:: shell-session
    $ python -m meta_package_manager
Removes empty string and current working directory from the first entry of
`sys.path`, if present to avoid using current directory
in subcommands when invoked as `python -m meta_package_manager <command>`.
"""

from __future__ import annotations

import os
import sys

import click

# if sys.path[0] in ("", os.getcwd()):
#    sys.path.pop(0)

from click import Context, echo, group, pass_context

from ocx_schema_reader import __version__
from ocx_schema_reader.cli import schema

WELCOME_MSG = "Hello!"
EXIT_MSG = "Goodbye!"


# @shell(prompt=f'CLI > ', intro=f'Starting CLI...')


@group(no_args_is_help=False, add_help_option=False, invoke_without_command=True)
@pass_context
def cli(ctx):
    """
    @shell(<name>) creates a shell utility of all click commands.
    @click.argument(<argument name>) tells us that we will be passing an argument
    and referring to that argument in the function by the name we pass it
    @click.pass_context tells the group command that we're going to be using
    the context, the context is not visible to the command unless we pass this
    """
    pass


def print_help_msg(command):
    with Context(command) as ctx:
        echo(command.get_help(ctx))


@cli.command()
def help():
    """Show help messages."""
    echo(print_help_msg(cli))


@cli.command()
def clear():
    """Clear the console window."""
    click.clear()


@cli.command("exit")
def quitapp():
    """Exit the CLI."""
    global quitapp
    quitapp = True


cli.add_command(schema)
""" The schema sub-commands """


def run_cli_prompt():
    args = sys.argv
    if args and (args[-1] == "--version"):
        print(f"CLI v{__version__}")
        return
    try:
        print(WELCOME_MSG)
        while not quitapp:
            astr = input("CLI > ")
            try:
                cli(astr.split())
            except SystemExit:
                # trap argparse error message
                # print('error', SystemExit)
                continue
            except Exception as e:
                echo(message=f"Error occurred!\n{str(e)}", err=True)
        print(EXIT_MSG)
    except (KeyboardInterrupt, EOFError):
        print(EXIT_MSG)
        sys.exit(0)


if __name__ == "main":
    quitapp = False  # global flag
    run_cli_prompt()
    # from ocx_schema_reader.cli import schema
    # Execute the CLI but force its name to not let Click defaults to:
    # "python -m ocx_schema_reader".
    # schema(prog_name=schema.name)

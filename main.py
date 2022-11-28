#  Copyright (c) 3-3Docx.org. See the LICENSE.

import logging
from logging import config
from pathlib import Path

import colorlog
from click_shell import shell

import ocx_schema_reader.schema_cli as schema_cli
from ocx_schema_reader.utils import ROOT_DIR, load_yaml_config

LOG_CONFIG_YAML = Path(ROOT_DIR) / "log_config.yaml"
log_config = load_yaml_config(LOG_CONFIG_YAML)
APP_CONFIG = Path(ROOT_DIR) / "config.yaml"
app_config = load_yaml_config(APP_CONFIG)
LOG_FOLDER = app_config.get("LOG_FOLDER")
Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)
INFO_COLOR = app_config.get("INFO_COLOR")
ERROR_COLOR = app_config.get("ERROR_COLOR")
LOG_LEVEL = app_config.get("LOG_LEVEL")
APP = app_config.get("APP")

# Set the logging configuration
config.dictConfig(log_config)
bold_seq = "\033[1m"
colorlog_format = f"{bold_seq} " "%(log_color)s " f"{log_config.get('formatters').get('std_out').get('format')}"
colorlog.basicConfig(format=colorlog_format)


log = logging.getLogger()  # Todo: Color logging does not work from main.py


@shell(prompt=f"{APP} > ", intro=f"{APP} commands")
def cli():
    pass


cli.add_command(schema_cli.schema)
""" The schema sub-commands """


if __name__ == "__main__":  # pragma: no cover
    cli()

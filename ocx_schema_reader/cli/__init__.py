#  Copyright (c) 2023.  OCX Consortium https://3docx.org. See the LICENSE

from pathlib import Path
from ocx_schema_reader import utils

config_folder = Path(utils.root_dir()) / "configs"
config_file = config_folder / "cli_config.yaml"
config = utils.load_yaml_config(config_file)

INFO_COLOR = config.get("INFO_COLOR")
ERROR_COLOR = config.get("ERROR_COLOR")
APP = config.get("APP")

log_config_file = config_folder / "log_config.yaml"
log_config = utils.load_yaml_config(log_config_file)

hndle = log_config["handlers"].get("file")
LOG_FILE = hndle.get("filename")

#  Copyright (c) 2023.  OCX Consortium https://3docx.org. See the LICENSE
from pathlib import Path
from ocx_schema_reader import utils

config = Path(utils.current_dir(__file__)) / "config.yaml"
MODULE_CONFIG = config.absolute()

app_config = utils.load_yaml_config(MODULE_CONFIG)

DEFAULT_SCHEMA = app_config.get("DEFAULT_SCHEMA")
SCHEMA_FOLDER = app_config.get("SCHEMA_FOLDER")
W3C_SCHEMA_BUILT_IN_TYPES = app_config.get("W3C_SCHEMA_BUILT_IN_TYPES")
PROCESS_SCHEMA_TYPES = app_config.get("PROCESS_SCHEMA_TYPES")
APP = app_config.get("APP")

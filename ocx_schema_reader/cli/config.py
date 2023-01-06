#  Copyright (c) 2023.  OCX Consortium https://3docx.org. See the LICENSE

from pathlib import Path
from ocx_schema_reader import utils

MODULE_CONFIG = Path(utils.root_dir()) / "config.yaml"
config = utils.load_yaml_config(MODULE_CONFIG)

INFO_COLOR = config.get("INFO_COLOR")
ERROR_COLOR = config.get("ERROR_COLOR")
APP = config.get("APP")

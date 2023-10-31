import os
import yaml
from sfpro.utils import logger
import json
from pathlib import Path
from typing import Any
from snowflake.snowpark import Row
from snowflake.snowpark.functions import udf
from snowflake.snowpark import Session

def collection_to_list(rows:list=None) -> list:
    return [list(i.as_dict().values())[0] for i in rows]


def read_yaml(path_to_yaml: Path):
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        raise e
    
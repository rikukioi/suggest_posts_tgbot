import logging.config

from pathlib import Path

import yaml


def configure_logger() -> None:
    with Path.open("logging_conf.yml") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config=config)

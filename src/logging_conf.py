import logging.config

from pathlib import Path

import yaml


def configure_logger() -> None:
    """Конфигурирует логгирование на глобальном уровне по конфигу (см. logging_conf.yml)."""
    logs_dir = Path("src/logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    config_file = Path("src/logging_conf.yml")
    with config_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config=config)

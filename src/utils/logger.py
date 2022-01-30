import os
import sys
from dataclasses import dataclass
from logging import Formatter, Handler, Logger, StreamHandler, getLogger

import coloredlogs


@dataclass
class Logger:

    name: str
    log_level: str = os.getenv("LOG_LEVEL", "DEBUG")
    formatter: Formatter = Formatter(
        "%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s"
    )

    def _get_console_handler(self) -> Handler:
        console_handler = StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_logger(self) -> Logger:
        logger = getLogger(self.name)
        logger.setLevel(self.log_level)
        logger.addHandler(self._get_console_handler())
        coloredlogs.install(
            fmt="%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
            level=self.log_level,
            logger=logger,
        )
        return logger

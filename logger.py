import logging
from typing import Union


class Logger:

    LogHandler = logging.StreamHandler()
    LogHandler.setLevel(logging.INFO)
    LogHandler.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    logging.getLogger('').addHandler(LogHandler)

    ScrapingLogger = logging.getLogger("[WEB_SCRAPING]")
    DatabaseLogger = logging.getLogger("[DATABASE_CONNECTION]")

    @staticmethod
    def set_scraping_log_level(log_level: Union[int, str]) -> None:
        Logger.ScrapingLogger.log(level=logging.CRITICAL, msg=f" Web Scraping Logger's level was changed from {Logger.ScrapingLogger.level} to {log_level}")
        Logger.ScrapingLogger.setLevel(log_level)

    @staticmethod
    def set_database_log_level(log_level: Union[int, str]) -> None:
        Logger.ScrapingLogger.log(level=logging.CRITICAL, msg=f" Web Scraping Logger's level was changed from {Logger.DatabaseLogger.level} to {log_level}")
        Logger.ScrapingLogger.setLevel(log_level)
import logging
from typing import Union
import datetime
import time


class Logger:


    def __init__(self):
        launch_time = datetime.datetime.now()
        logging.basicConfig(
            filename=f'ftb2-{launch_time.date().__str__()}-{launch_time.time().hour}-{launch_time.time().minute}-{launch_time.time().second}.log',
            filemode='w',
            level=logging.INFO,
            format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        )
        self.ScrapingLogger = logging.getLogger("[WEB_SCRAPING]")
        self.DatabaseLogger = logging.getLogger("[DATABASE_CONNECTION]")
        self.PlayerScrapingLogger = logging.getLogger("[PLAYER_SCRAPING]")
        self.ConfigurationLogger = logging.getLogger("[CONFIGURATION]")

    def set_scraping_log_level(self, log_level: Union[int, str]):
        self.ScrapingLogger.log(level=logging.CRITICAL, msg=f" Web Scraping Logger's level was changed from {self.ScrapingLogger.level} to {log_level}")
        self.ScrapingLogger.setLevel(log_level)

    def set_database_log_level(self, log_level: Union[int, str]) -> None:
        self.ScrapingLogger.log(level=logging.CRITICAL, msg=f" Web Scraping Logger's level was changed from {self.DatabaseLogger.level} to {log_level}")
        self.ScrapingLogger.setLevel(log_level)
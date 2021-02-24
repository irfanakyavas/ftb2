import logging
import time

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions

import sqlconnection
from attrs_scraper import PlayerDataScraper
from config import ConfigHandler
from logger import Logger
from matchdatascrapping import MatchDataScraper
from scrapeoptions import DriverType, League
from sqlconnection import SQLConnection

SCRAPING_WEBDRIVER = None
SCRAPING_WEBDRIVER_OPTIONS = None

logger_instance = Logger()
MainLogger = logging.getLogger("[MAIN]")
config_handler = ConfigHandler()


def initialize_ftb2():
    global SCRAPING_WEBDRIVER
    global SCRAPING_WEBDRIVER_OPTIONS

    if config_handler.database_use == '1':
        MainLogger.info("Connecting to SQL Database as specified by configuration file.")
        sql = SQLConnection.get_or_init_sql_connection(sqlconnection.from_config_handler())
        sql.load_team_id_map()
        sql.update_team_id_name_mapping_on_db()
    else:
        MainLogger.info("NOT connecting to SQL Database as specified by configuration file.")

    if config_handler.scrape_webdriver == "FIREFOX":
        SCRAPING_WEBDRIVER = DriverType.FIREFOX
        SCRAPING_WEBDRIVER_OPTIONS = FirefoxOptions()
    elif config_handler.scrape_webdriver == "OPERA":
        SCRAPING_WEBDRIVER = DriverType.OPERA
        SCRAPING_WEBDRIVER_OPTIONS = OperaOptions()
    elif config_handler.scrape_webdriver == "CHROME":
        SCRAPING_WEBDRIVER = DriverType.CHROME
        SCRAPING_WEBDRIVER_OPTIONS = ChromeOptions()

    SCRAPING_WEBDRIVER_OPTIONS.headless = True if config_handler.scrape_is_headless == "1" else False


def main():
    #initialize_ftb2()
    time_start = time.time()
    scraper = PlayerDataScraper()
    all_players_in_pl = scraper.scrape_players(League.EN_PREMIER_LEAGUE)
    print(f"{len(all_players_in_pl)} players scraped in {time.time() - time_start} seconds")
    for p in all_players_in_pl:
        print(p)


if __name__ == "__main__":
    main()

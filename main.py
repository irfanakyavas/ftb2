import logging
import time

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions

import sqlconnection
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

if config_handler.database_use is '1':
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

SCRAPING_WEBDRIVER_OPTIONS.headless = True if config_handler.scrape_is_headless is "1" else False

scraper = MatchDataScraper(SCRAPING_WEBDRIVER, SCRAPING_WEBDRIVER_OPTIONS)
start_time = time.time()
all_matches = scraper.scrape_league(League.EN_PREMIER_LEAGUE, scrape_range=slice(0, 3))
for match in all_matches:
    print(match)

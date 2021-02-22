import sqlconnection
from matchdatascrapping import MatchDataScraper
from sqlconnection import SQLConnection
from config import ConfigHandler
from logger import Logger
import logging
import time
from scrapeoptions import DriverType


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

SCRAPING_WEBDRIVER = None

if config_handler.scrape_webdriver == "FIREFOX":
    SCRAPING_WEBDRIVER = DriverType.FIREFOX
elif config_handler.scrape_webdriver == "OPERA":
    SCRAPING_WEBDRIVER = DriverType.OPERA
elif config_handler.scrape_webdriver == "CHROME":
    SCRAPING_WEBDRIVER = DriverType.CHROME

manu_players = sql.load_players_by_team_name("Manchester Utd") #şimdi API'ı kullanabilirsin
print(manu_players[0])
#scraper = MatchDataScraper(SCRAPING_WEBDRIVER, config_handler.scrape_is_headless)

#start_time = time.time()
#all_matches = scraper.scrape_league(MatchDataScraper.League.EN_PREMIER_LEAGUE, scrape_range=slice(0, 3))
#for match in all_matches:
#    print(match)
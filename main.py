import sqlconnection
from matchdatascrapping import MatchDataScraper
from sqlconnection import SQLConnection
from config import ConfigHandler
import logger
from logger import Logger
import logging
import time

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

scraper = MatchDataScraper(MatchDataScraper.DriverType.FIREFOX)
start_time = time.time()
all_matches = scraper.scrape_league(MatchDataScraper.League.EN_PREMIER_LEAGUE, scrape_range=slice(0, 3))
for match in all_matches:
    print(match)
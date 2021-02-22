import sqlconnection
from matchdatascrapping import MatchDataScraper
from sqlconnection import SQLConnection
from sqlconnection import SQLLogin
from config import ConfigHandler
import logger
import time


scrape_logger = logger.Logger()
config_handler = ConfigHandler()
sql = SQLConnection.get_or_init_sql_connection(sqlconnection.from_config_handler())
sql.load_team_id_map()
sql.update_team_id_name_mapping_on_db()
alisson = sql.load_player_by_id(30)
print(alisson)

#scraper = MatchDataScraper(MatchDataScraper.DriverType.FIREFOX)
#start_time = time.time()
#all_matches = scraper.scrape_league(MatchDataScraper.League.EN_PREMIER_LEAGUE, scrape_range=slice(0, 15))
#print("all matches processed in %s seconds (Full names)" % (time.time() - start_time))
print("map loaded")
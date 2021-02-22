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

#scraper = MatchDataScraper(MatchDataScraper.DriverType.FIREFOX)
#start_time = time.time()
#all_matches = scraper.scrape_league(MatchDataScraper.League.EN_PREMIER_LEAGUE, scrape_range=slice(0, 15))
#print("all matches processed in %s seconds (Full names)" % (time.time() - start_time))
all_matches = sql.load_matches_by_club_name("Fulham")
for match in all_matches:
    print(match)
#sql.save_matches(all_matches)
print("map loaded")
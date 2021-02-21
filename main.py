from scrape_league import MatchDataScraper
import time
import team
from sql_connection import SQL_Connection
from sql_connection import SQL_Login
import logger
from config import ConfigHandler

scrape_logger = logger.Logger()
config_handler = ConfigHandler()
sql = SQL_Connection.get_or_init_sql_connection(SQL_Login.from_config_handler())
sql.load_team_id_map()

scraper = MatchDataScraper(MatchDataScraper.DriverType.FIREFOX)
start_time = time.time()
all_matches = scraper.scrape_league(MatchDataScraper.League.EN_PREMIER_LEAGUE, scrape_range=slice(0, 15))
print("all matches processed in %s seconds (Full names)" % (time.time() - start_time))
for match in all_matches:
    print(match)

print("map loaded")
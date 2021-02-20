import scrape_league
from scrape_league import MatchDataScraper
import time
import team
from sql_connection import SQL_Connection
import logger

scrape_logger = logger.Logger()

scraper = MatchDataScraper(MatchDataScraper.DriverType.FIREFOX)
start_time = time.time()
all_matches = scraper.scrape_league(MatchDataScraper.League.EN_PREMIER_LEAGUE, scrape_range=slice(0, 15))
print("all matches processed in %s seconds (Full names)" % (time.time() - start_time))
for match in all_matches:
    print(match)
sql = SQL_Connection()
sql.save_matches(all_matches)
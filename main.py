import scrape_league
import time
import team
from sql_connection import SQL_Connection

start_time = time.time()
all_matches = scrape_league.scrape_league("firefox", "england", "premier-league")
print("all matches processed in %s seconds (Full names)" % (time.time() - start_time))
for match in all_matches:
    print(match)
sql = SQL_Connection()
sql.save_matches(all_matches)
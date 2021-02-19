import scrape_league
import time


start_time = time.time()
all_matches = scrape_league.scrape_league("firefox", "england", "premier-league", True)
print("all matches processed in %s seconds (Full names)" % (time.time() - start_time))
start_time2 = time.time()
all_matches2 = scrape_league.scrape_league("firefox", "england", "premier-league", False)
print("all matches processed in %s seconds (Partial names)" % (time.time() - start_time2))
for match in all_matches:
    print(match)

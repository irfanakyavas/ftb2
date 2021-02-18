import scrape_league

all_matches = scrape_league.scrape_league("firefox", "england", "premier-league")
for match in all_matches:
    print(match)
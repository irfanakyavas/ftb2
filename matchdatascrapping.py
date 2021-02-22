import selenium
from selenium import webdriver
import time

from selenium.webdriver.support import wait
import sys
from team import *
from match import Match
from match import MatchResult
from lxml import html
import requests
from enum import Enum
from logger import Logger
import logging
from selenium.common.exceptions import *

SCRAPE_LOGGER = logging.getLogger("[WEB_SCRAPING]")


class MatchDataScraper:
    class League(Enum):
        EN_PREMIER_LEAGUE = ("england", "premier-league")
        TR_SUPER_LEAGUE = ("turkey", "super-lig")

    class DriverType(Enum):
        FIREFOX = 1
        CHROME = 2
        OPERA = 3

    def __init__(self, driver_type: DriverType):
        global SCRAPE_LOGGER
        # Logging & initialization for Firefox webdriver
        if driver_type == MatchDataScraper.DriverType.FIREFOX:
            SCRAPE_LOGGER.info("Firefox Web Driver was chosen for Selenium, trying to initialize.")
            try:
                self.driver = selenium.webdriver.Firefox()
            except selenium.common.exceptions.WebDriverException:
                SCRAPE_LOGGER.critical(
                    "COULD NOT initialize Firefox Web Driver, is Firefox Web Driver present in path variable?.")
                sys.exit(1)
            else:
                SCRAPE_LOGGER.info("Firefox Web Driver was successfully initialized.")

        # Logging & initialization for Chrome webdriver
        if driver_type == MatchDataScraper.DriverType.CHROME:
            SCRAPE_LOGGER.info("Chrome Web Driver was chosen for Selenium, trying to initialize.")
            try:
                self.driver = selenium.webdriver.Chrome()
            except selenium.common.exceptions.WebDriverException:
                SCRAPE_LOGGER.critical(
                    "COULD NOT initialize Chrome Web Driver, is Chrome Web Driver present in path variable?.")
                sys.exit(1)
            else:
                SCRAPE_LOGGER.info("Chrome Web Driver was successfully initialized.")

        # Logging & initialization for Opera webdriver
        if driver_type == MatchDataScraper.DriverType.OPERA:
            SCRAPE_LOGGER.info(logging.INFO, "Opera Web Driver was chosen for Selenium, trying to initialize.")
            try:
                self.driver = selenium.webdriver.Opera()
            except selenium.common.exceptions.WebDriverException:
                SCRAPE_LOGGER.critical(
                    "COULD NOT initialize Opera Web Driver, is Opera Web Driver present in path variable?.")
                sys.exit(1)
            else:
                SCRAPE_LOGGER.info("Opera Web Driver was successfully initialized.")

    def html_to_matchids(self, elem):
        return elem.get_attribute("id")[4:]  # First 4 characters of flashscore.com match ids have no use

    def get_player_full_name(self, player_url):
        player_page = requests.get(f'https://www.flashscore.com{player_url}')
        tree = html.fromstring(player_page.content)
        player_full_name = tree.cssselect(".teamHeader__name")[0].text.split('\n')[0]
        return player_full_name

    def parse_lineups(self, lineups_table, match, use_full_names=False):
        lineup_rows = lineups_table.find_elements_by_tag_name("tr")[1:12]

        for lineup_row in lineup_rows:
            if use_full_names:
                home_player_full_name_url = \
                    lineup_row.find_element_by_class_name("summary-vertical.fl").find_element_by_class_name(
                        "name").find_element_by_tag_name("a").get_attribute("onclick").split("'")[1]
                away_player_full_name_url = \
                    lineup_row.find_element_by_class_name("summary-vertical.fr").find_element_by_class_name(
                        "name").find_element_by_tag_name("a").get_attribute("onclick").split("'")[1]
                home_player = self.get_player_full_name(home_player_full_name_url)
                away_player = self.get_player_full_name(away_player_full_name_url)
            else:
                home_player = lineup_row.find_element_by_class_name("summary-vertical.fl") \
                    .find_element_by_class_name("name").text.strip()
                away_player = lineup_row.find_element_by_class_name("summary-vertical.fr") \
                    .find_element_by_class_name("name").text.strip()

            match.home_team_lineup.append(home_player)
            match.away_team_lineup.append(away_player)

    def parse_statistics(self, stat_rows, match):
        for stat_row in stat_rows:
            stat_name = stat_row.find_element_by_class_name("statText.statText--titleValue").text
            if stat_name == "Ball Possession":
                match.ball_possession[0] = float(
                    stat_row.find_element_by_class_name("statText.statText--homeValue").text[:2]) / 100
                match.ball_possession[1] = float(
                    stat_row.find_element_by_class_name("statText.statText--awayValue").text[:2]) / 100
            if stat_name == "Goal Attempts":
                match.goal_attempts[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.goal_attempts[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Shots on Goal":
                match.shots_on_goal[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.shots_on_goal[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Shots off Goal":
                match.shots_off_goal[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.shots_off_goal[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Blocked Shots":
                match.blocked_shots[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.blocked_shots[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Free Kicks":
                match.free_kicks[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.free_kicks[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Corner Kicks":
                match.corner_kicks[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.corner_kicks[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Offsides":
                match.offsides[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.offsides[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Goalkeeper Saves":
                match.goalkeeper_saves[0] = int(
                    stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.goalkeeper_saves[1] = int(
                    stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Fouls":
                match.fouls[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.fouls[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Red Cards":
                match.red_cards[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.red_cards[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Yellow Cards":
                match.yellow_cards[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.yellow_cards[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Total Passes":
                match.total_passes[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.total_passes[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Tackles":
                match.tackles[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.tackles[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Attacks":
                match.attacks[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.attacks[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
            if stat_name == "Dangerous Attacks":
                match.dangerous_attacks[0] = int(
                    stat_row.find_element_by_class_name("statText.statText--homeValue").text)
                match.dangerous_attacks[1] = int(
                    stat_row.find_element_by_class_name("statText.statText--awayValue").text)

    def match_id_to_match(self, matchid, use_full_names=False):
        SCRAPE_LOGGER.info("Starting to parse a match, loading match page.")
        self.driver.get(f"https://www.flashscore.com/match/{matchid}/#match-statistics;0")
        time.sleep(2)

        home_team = Team.get_or_create_team(
            self.driver.find_element_by_class_name("team-text.tname-home").find_element_by_class_name(
                "participant-imglink").text)
        away_team = Team.get_or_create_team(
            self.driver.find_element_by_class_name("team-text.tname-away").find_element_by_class_name(
                "participant-imglink").text)

        match = Match(home_team, away_team)

        score_box = self.driver.find_element_by_id("event_detail_current_result")
        scores = score_box.find_elements_by_class_name("scoreboard")
        match.scores = list(map(lambda score_element: int(score_element.text), scores))

        stat_rows = self.driver.find_elements_by_class_name("statRow")
        self.parse_statistics(stat_rows, match)

        self.driver.get(f"https://www.flashscore.com/match/{matchid}/#lineups;1")
        time.sleep(1.25)

        lineups_table = self.driver.find_element_by_css_selector(
            ".lineups-wrapper > table:nth-child(1) > tbody:nth-child(1)")
        self.parse_lineups(lineups_table, match, use_full_names=use_full_names)

        home_team.matches.append(match)
        away_team.matches.append(match)

        match.match_result = MatchResult.DRAW
        if match.scores[0] > match.scores[1]:
            match.match_result = MatchResult.HOME_WIN
        if match.scores[0] < match.scores[1]:
            match.match_result = MatchResult.AWAY_WIN

        SCRAPE_LOGGER.info(f"Match between {home_team.team_name} and {away_team.team_name} is parsed")
        return match

    def remove_cookie_banner(self):
        try:
            trust_banner = self.driver.find_element_by_xpath('//*[@id="onetrust-banner-sdk"]')
            self.driver.execute_script("arguments[0].style.visibility='hidden'", trust_banner)

        except NoSuchElementException:
            Logger.ScrapingLogger.log(level=logging.INFO, msg="No FlashScore Cookie consent banner to remove.")

    def scrape_league(self, league: League, scrape_range: slice = slice(0, None), use_full_names=False):

        SCRAPE_LOGGER.info(f"scrape_league was called on {league.value} for {scrape_range.__str__()}")

        self.driver.get(url=f"https://www.flashscore.com/football/{league.value[0]}/{league.value[1]}/results/")

        SCRAPE_LOGGER.info(f"WebDriver is now waiting for the cookie consent banner to appear")
        wait.WebDriverWait(driver=self.driver, timeout=1000).until(
            lambda t: t.find_element_by_xpath('//*[@id="onetrust-banner-sdk"]'))
        self.remove_cookie_banner()
        SCRAPE_LOGGER.info(f"Removed the cookie consent banner")

        all_matches_box = self.driver.find_element_by_class_name("sportName.soccer")

        SCRAPE_LOGGER.info(f"WebDriver is now clicking show more matches button")
        num_pages = 1
        while True:
            try:
                show_more_button = self.driver.find_element_by_class_name("event__more.event__more--static")
                show_more_button.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                SCRAPE_LOGGER.error(f"Cookie consent banner somehow appeared again. Trying to remove it again.")
                self.remove_cookie_banner()
                time.sleep(0.1)
                continue
            except NoSuchElementException:
                SCRAPE_LOGGER.info(
                    f"WebDriver revealed all matches, {num_pages} of match pages were revealed after {num_pages - 1} button clicks")
                break
            else:
                num_pages = num_pages + 1

        SCRAPE_LOGGER.info(f"WebDriver will now collect all match elements for further processing to get match ids")
        all_matches_elements = all_matches_box.find_elements_by_class_name(
            "event__match.event__match--static.event__match--oneLine")

        SCRAPE_LOGGER.info(f"Trying to map match elements to match ids")
        all_match_ids = list(map(self.html_to_matchids, all_matches_elements))
        SCRAPE_LOGGER.info(f"Match id collection completed")

        SCRAPE_LOGGER.info(f"Trying to scrape lineup and statistics using match ids")
        if use_full_names:
            all_matches = [self.match_id_to_match(matchid=match_id, use_full_names=True) for match_id in
                           all_match_ids[scrape_range]]
        else:
            all_matches = [self.match_id_to_match(matchid=match_id, use_full_names=False) for match_id in
                           all_match_ids[scrape_range]]
        SCRAPE_LOGGER.info(f"Scraping completed")
        return all_matches

import selenium
from selenium import webdriver
import time
from team import *
from match import *
from lxml import html
import requests

try:
    driver = webdriver.Firefox()
except:
    print("No firefox driver found")

def html_to_matchids(elem):
    return elem.get_attribute("id")[4:]


def get_player_full_name(player_url):
    player_page = requests.get(f'https://www.flashscore.com{player_url}')
    tree = html.fromstring(player_page.content)
    player_full_name = tree.cssselect(".teamHeader__name")[0].text.split('\n')[0]
    return player_full_name


def parse_lineups(lineups_table, match, use_full_names=False):
    lineup_rows = lineups_table.find_elements_by_tag_name("tr")[1:12]

    for lineup_row in lineup_rows:
        if use_full_names:
            home_player_full_name_url = \
                lineup_row.find_element_by_class_name("summary-vertical.fl").find_element_by_class_name(
                    "name").find_element_by_tag_name("a").get_attribute("onclick").split("'")[1]
            away_player_full_name_url = \
                lineup_row.find_element_by_class_name("summary-vertical.fr").find_element_by_class_name(
                    "name").find_element_by_tag_name("a").get_attribute("onclick").split("'")[1]
            home_player = get_player_full_name(home_player_full_name_url)
            away_player = get_player_full_name(away_player_full_name_url)
        else:
            home_player = lineup_row.find_element_by_class_name("summary-vertical.fl") \
                .find_element_by_class_name("name").text.strip()
            away_player = lineup_row.find_element_by_class_name("summary-vertical.fr") \
                .find_element_by_class_name("name").text.strip()

        match.home_team_lineup.append(home_player)
        match.away_team_lineup.append(away_player)


def parse_statistics(stat_rows, match):
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
            match.goalkeeper_saves[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
            match.goalkeeper_saves[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)
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
            match.dangerous_attacks[0] = int(stat_row.find_element_by_class_name("statText.statText--homeValue").text)
            match.dangerous_attacks[1] = int(stat_row.find_element_by_class_name("statText.statText--awayValue").text)


def match_id_to_match(matchid):
    driver.get(f"https://www.flashscore.com/match/{matchid}/#match-statistics;0")
    time.sleep(2)

    home_team = Team.get_or_create_team(driver.find_element_by_class_name("team-text.tname-home").find_element_by_class_name(
            "participant-imglink").text)
    away_team = Team.get_or_create_team(driver.find_element_by_class_name("team-text.tname-away").find_element_by_class_name(
            "participant-imglink").text)

    match = Match(home_team, away_team)

    score_box = driver.find_element_by_id("event_detail_current_result")
    scores = score_box.find_elements_by_class_name("scoreboard")
    match.scores = list(map(lambda score_element: int(score_element.text), scores))

    stat_rows = driver.find_elements_by_class_name("statRow")
    parse_statistics(stat_rows, match)

    driver.get(f"https://www.flashscore.com/match/{matchid}/#lineups;1")
    time.sleep(1.25)

    lineups_table = driver.find_element_by_css_selector(".lineups-wrapper > table:nth-child(1) > tbody:nth-child(1)")
    parse_lineups(lineups_table, match)

    home_team.matches.append(match)
    away_team.matches.append(match)

    return match


def match_id_to_match_full_names(matchid):
    driver.get(f"https://www.flashscore.com/match/{matchid}/#match-statistics;0")
    time.sleep(1.5)

    home_team = Team.get_or_create_team(
        driver.find_element_by_class_name("team-text.tname-home").find_element_by_class_name(
            "participant-imglink").text)
    away_team = Team.get_or_create_team(
        driver.find_element_by_class_name("team-text.tname-away").find_element_by_class_name(
            "participant-imglink").text)

    match = Match(home_team, away_team)

    score_box = driver.find_element_by_id("event_detail_current_result")
    scores = score_box.find_elements_by_class_name("scoreboard")
    match.scores = list(map(lambda score_element: int(score_element.text), scores))

    stat_rows = driver.find_elements_by_class_name("statRow")
    parse_statistics(stat_rows, match)

    driver.get(f"https://www.flashscore.com/match/{matchid}/#lineups;1")
    time.sleep(1.25)

    lineups_table = driver.find_element_by_css_selector(".lineups-wrapper > table:nth-child(1) > tbody:nth-child(1)")
    parse_lineups(lineups_table, match, True)

    home_team.matches.append(match)
    away_team.matches.append(match)

    return match


def scrape_league(driver_type, country, league, use_full_names=False):
    global driver
    if driver_type == "chrome":
        driver = webdriver.Chrome
        print("Alternating to chrome because of arguments")
    if driver_type == "opera":
        driver = webdriver.Opera
        print("Alternating to opera because of arguments")

    driver.get(url=f"https://www.flashscore.com/football/{country}/{league}/results/")
    time.sleep(3)

    try:
        trust_banner = driver.find_element_by_xpath('//*[@id="onetrust-banner-sdk"]')
        driver.execute_script("arguments[0].style.visibility='hidden'", trust_banner)
    except selenium.common.exceptions.NoSuchElementException:
        print("No cookie consent banner to remove")

    all_matches_box = driver.find_element_by_class_name("sportName.soccer")
    show_more_button = driver.find_element_by_class_name("event__more.event__more--static")

    num_pages = 1
    while show_more_button is not None:
        show_more_button.click()
        time.sleep(1.5)
        try:
            show_more_button = driver.find_element_by_class_name("event__more.event__more--static")
            num_pages = num_pages + 1
        except selenium.common.exceptions.StaleElementReferenceException:
            show_more_button = None
            break
        except selenium.common.exceptions.NoSuchElementException:
            show_more_button = None
            break

    all_matches_elements = all_matches_box.find_elements_by_class_name(
        "event__match.event__match--static.event__match--oneLine")

    all_match_ids = list(map(html_to_matchids, all_matches_elements))

    if use_full_names:
        all_matches = list(map(match_id_to_match_full_names, all_match_ids))
    else:
        all_matches = list(map(match_id_to_match, all_match_ids[:25]))  # Tüm maçları almak istiyorsan [:3] ü kaldır tüm match id leri gezsin baya uzun sürüyo ama oluyo
    return all_matches

# https://www.flashscore.com/match/[matchid]/#match-summary

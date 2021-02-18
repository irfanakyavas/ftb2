import selenium
from selenium import webdriver
import time
from team import *
from match import *


def remove_captain_goalkeeper_indicators(lineup_row, driver):
    goalkeeper_captain_indicator_elem = lineup_row.find_element_by_tag_name("span")
    driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""",  # TODO:(C) ve (G) kaldırma çalışmıyor
                          goalkeeper_captain_indicator_elem)


def parse_lineups(lineups_table, match, driver):
    lineup_rows = lineups_table.find_elements_by_tag_name("tr")[1:12]
    for lineup_row in lineup_rows:
        remove_captain_goalkeeper_indicators(lineup_row, driver)
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


def match_element_to_match(match_element):
    match_id = match_element.get_attribute("id")[4:]  # match id 4.karakter ile başlıyor

    driver.get(f"https://www.flashscore.com/match/{match_id}/#match-statistics;0")  # istatistik sayfasını yükle
    time.sleep(1)

    # takım isimlerini kaydet ve takım nesneleri oluştur
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

    driver.get(f"https://www.flashscore.com/match/{match_id}/#lineups;1")
    time.sleep(1)

    lineups_table = driver.find_element_by_css_selector(".lineups-wrapper > table:nth-child(1) > tbody:nth-child(1)")
    parse_lineups(lineups_table, match, driver)

    home_team.matches.append(match)
    away_team.matches.append(match)

    return match


driver = webdriver.Firefox()
driver.get("https://www.flashscore.com/football/england/premier-league/results/")
assert "Premier League 2020/2021 Results" in driver.title
time.sleep(3)

trust_banner = driver.find_element_by_xpath('//*[@id="onetrust-banner-sdk"]')  # Cookie acceptall bannerini görünmez yap
driver.execute_script("arguments[0].style.visibility='hidden'", trust_banner)

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
        print(f"Number of Match Pages is {num_pages}")
        show_more_button = None
        break
    except selenium.common.exceptions.NoSuchElementException:
        print(f"Number of Match Pages is {num_pages}")
        show_more_button = None
        break

all_matches_elements = all_matches_box.find_elements_by_class_name(
    "event__match.event__match--static.event__match--oneLine")

all_matches = list(map(match_element_to_match, all_matches_elements[:3]))  # sadece en yeni 3 maça bakıyorum, istersen sil hepsine bak ama baya uzun sürüyor
aml = list(all_matches)  # bu line'a breakpoint koyup debugger penceresinden all_matches'a bakabilirsin

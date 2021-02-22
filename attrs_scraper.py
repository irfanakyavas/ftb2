from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mariadb, sys, time
from config import ConfigHandler
from player import Player
from sqlconnection import SQLConnection, SQLLogin
import sqlconnection, scrapeoptions

db = SQLConnection.get_or_init_sql_connection(sqlconnection.from_config_handler())

options = Options()
options.headless = True

league_id = scrapeoptions.League.EN_PREMIER_LEAGUE['players']['league_id']
league_name = scrapeoptions.League.EN_PREMIER_LEAGUE['players']['league_name']
fm_version = scrapeoptions.League.EN_PREMIER_LEAGUE['players']['fm_version']
BASE_URL = f"https://fmdataba.com/{fm_version}/l/{league_id}/{league_name}/best-players/"
MAX_PAGE_INDEX = 13

def create_url(BASE_URL, pageIndex):
    url = BASE_URL + str(pageIndex)
    return url


def get_attrs(pageIndex):
    global club_name_container, player_name
    driver = webdriver.Chrome(options=options)
    url = create_url(BASE_URL, pageIndex)
    driver.get(url)
    print(url, "is opening")
    time.sleep(2)

    table = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/table/tbody")
    rows = table.find_elements_by_tag_name("tr")
    players = list()

    for row in rows:
        p = Player(player_team_name='', player_name='')
        elements = row.find_elements_by_tag_name("td")
        for index, element in enumerate(elements):
            if index == 2:
                player_name_container = element.find_element_by_tag_name("a")
                player_name = player_name_container.find_element_by_tag_name("strong")
                p.player_name = player_name.text
            if index == 3:
                club_name_container = element.find_element_by_tag_name("a")
                p.player_team_name = club_name_container.text
            # getting attributes except overall
            if index > 6:
                p.attributes[index - 7] = element.text
        if p.player_name != '':
            players.append(p)
    driver.quit()
    return players

def get_players():
    # MAX_PAGE_INDEX + 1
    for index in range(1, MAX_PAGE_INDEX):
        players = get_attrs(index)
        for player in players:
            if player.player_team_name == "Manchester Ci":
                player.player_team_name = "Manchester City"
            else:
                pass
            try:
                db.save_player(player)
            except:
                print("Error")

def start_player_scrapping():
    get_players()

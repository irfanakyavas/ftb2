import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import mariadb
import sys

DB_NAME = "football"
# Connect to MariaDB Platform
try:
    db = mariadb.connect(
        user="root",
        password="",
        host="127.0.0.1",
        port=3307,
        database=DB_NAME
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cursor = db.cursor()
db.autocommit = False

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

BASE_URL = "https://fmdataba.com/21/l/2613/premier-league/best-players/"
MAX_PAGE_INDEX = 12


def create_url(BASE_URL, pageIndex):
    url = BASE_URL + str(pageIndex)
    return url


def get_attrs(pageIndex):
    url = create_url(BASE_URL, pageIndex)
    driver.get(url)
    time.sleep(3)

    table = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/table/tbody")
    rows = table.find_elements_by_tag_name("tr")
    players = list()
    print(type(rows))
    for row in rows:
        player = list()
        elements = row.find_elements_by_tag_name("td")
        for index, element in enumerate(elements):
            if index == 2:
                player_name_container = element.find_element_by_tag_name("a")
                player_name = player_name_container.find_element_by_tag_name("strong")
                player.append(player_name.text)
            if index == 3:
                club_name_container = element.find_element_by_tag_name("a")
                player.append(club_name_container.text)
            # getting attributes except overall
            if index > 6:
                player.append(element.text)
        if len(player) > 0:
            players.append(player)
    driver.quit()
    return players

def get_players():
    # MAX_PAGE_INDEX + 1
    for index in range(1,3):
        players = get_attrs(index)
        for player in players:
            if player[1] == "Manchester Ci":
                player[1] = "Manchester City"
            else:pass
            print(player)
            try:
                query = cursor.execute('INSERT INTO players VALUES(?,?,?,?,?,?,?,?,?)',
                        ("NULL", player[0], player[1], int(player[2]), int(player[3]), int(player[4]),
                            int(player[5]), int(player[6]), int(player[7])))
                print(str(query), player[0], "added")

            except:
                print("Error")
    db.commit()

#get_players()
print(get_attrs(1))

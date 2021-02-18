import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

BASE_URL = "https://fmdataba.com/21/l/2613/premier-league/best-players/"
# premier lig oyuncuları için linkteki toplam sayfa sayısı 
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
            print(player)


for index in range(MAX_PAGE_INDEX + 1):
    get_attrs(index)

driver.quit()

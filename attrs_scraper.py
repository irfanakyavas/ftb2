import logging
import sys
import time
from typing import Union

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions

from player import Player
from scrapeoptions import DriverType
from scrapeoptions import League


class PlayerDataScraper:
    SCRAPE_LOGGER = logging.getLogger("WEB_SCRAPING")
    MAX_PAGE_INDEX = 13

    base_url = None
    league_id = None
    league_name = None
    fm_version = None

    def __init__(self, driver_type: DriverType,
                 driver_options: Union[FirefoxOptions, OperaOptions, ChromeOptions, None]):

        # Logging & initialization for Firefox webdriver
        if driver_type == DriverType.FIREFOX:
            PlayerDataScraper.SCRAPE_LOGGER.info("Firefox Web Driver was chosen for Selenium, trying to initialize.")
            try:
                self.driver = selenium.webdriver.Firefox(options=driver_options)
            except selenium.common.exceptions.WebDriverException:
                PlayerDataScraper.SCRAPE_LOGGER.critical(
                    "COULD NOT initialize Firefox Web Driver, is Firefox Web Driver present in path variable?.")
                sys.exit(1)
            else:
                PlayerDataScraper.SCRAPE_LOGGER.info("Firefox Web Driver was successfully initialized.")

        # Logging & initialization for Chrome webdriver
        if driver_type == DriverType.CHROME:
            PlayerDataScraper.SCRAPE_LOGGER.info("Chrome Web Driver was chosen for Selenium, trying to initialize.")
            try:
                self.driver = selenium.webdriver.Chrome(options=driver_options)
            except selenium.common.exceptions.WebDriverException:
                PlayerDataScraper.SCRAPE_LOGGER.critical(
                    "COULD NOT initialize Chrome Web Driver, is Chrome Web Driver present in path variable?.")
                sys.exit(1)
            else:
                PlayerDataScraper.SCRAPE_LOGGER.info("Chrome Web Driver was successfully initialized.")

        # Logging & initialization for Opera webdriver
        if driver_type == DriverType.OPERA:
            PlayerDataScraper.SCRAPE_LOGGER.info(logging.INFO,
                                                 "Opera Web Driver was chosen for Selenium, trying to initialize.")
            try:
                self.driver = selenium.webdriver.Opera(options=driver_options)
            except selenium.common.exceptions.WebDriverException:
                PlayerDataScraper.SCRAPE_LOGGER.critical(
                    "COULD NOT initialize Opera Web Driver, is Opera Web Driver present in path variable?.")
                sys.exit(1)
            else:
                PlayerDataScraper.SCRAPE_LOGGER.info("Opera Web Driver was successfully initialized.")

    def create_url(BASE_URL, pageIndex):
        url = BASE_URL + str(pageIndex)
        return url

    def get_attrs(self, pageIndex):
        global club_name_container, player_name

        url = self.create_url(PlayerDataScraper.base_url, pageIndex)
        self.driver.get(url)
        print(url, "is opening")
        time.sleep(2)

        table = self.driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]/table/tbody")
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
        self.driver.quit()
        return players

    def get_players(self):
        # MAX_PAGE_INDEX + 1
        return_players_list = []
        for index in range(1, PlayerDataScraper.MAX_PAGE_INDEX):
            players = self.get_attrs(index)
            for player in players:
                if player.player_team_name == "Manchester Ci":
                    player.player_team_name = "Manchester City"
                else:
                    pass
                try:
                    return_players_list.append(player)
                except:
                    print("Error")

        return return_players_list

    def scrape_players(self, league: League, max_page_index: int):
        PlayerDataScraper.MAX_PAGE_INDEX = max_page_index
        PlayerDataScraper.league_id = league['players']['league_id']
        PlayerDataScraper.league_name = league['players']['league_name']
        PlayerDataScraper.fm_version = league['players']['fm_version']
        PlayerDataScraper.base_url = f"https://fmdataba.com/{PlayerDataScraper.fm_version}/l/" \
                                     f"{PlayerDataScraper.league_id}/{PlayerDataScraper.league_name}/best-players/"

        return self.get_players()

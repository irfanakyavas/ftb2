import logging
import time
from typing import List, Dict, Optional
from player import Player
from scrapeoptions import League
import requests
import lxml
from lxml import html
from lxml.cssselect import CSSSelector
from lxml import etree


class PlayerDataScraper:
    SCRAPE_LOGGER = logging.getLogger("[WEB_SCRAPING]")

    def __init__(self):
        print("initializing player scrapper")

    def get_player_data(self, base_url: str, page_index: int = 0, players_return_list=None,
                        team_names_fix_dict: Dict[str, str] = None) -> Optional[List[Player]]:
        if players_return_list is None:
            players_return_list = list()

        fake_useragent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
        players_page = requests.get(base_url + str(page_index), headers=fake_useragent)
        players_page_elements = html.fromstring(players_page.content)
        players_table = players_page_elements.cssselect('.table-responsive > table:nth-child(1) > tbody:nth-child(2)')[
            0]
        num_player_rows = 0

        for player_row in players_table.iter("tr"):
            if player_row.find('.//td[3]/a/strong') is None:
                continue

            player_name = player_row.find('.//td[3]/a/strong').text
            player_team_name = player_row.find('.//td[4]/a/span').text

            for (team_name_to_fix, team_name_fixed) in team_names_fix_dict.items():
                if player_team_name == team_name_to_fix:
                    player_team_name = team_name_fixed

            p = Player(player_team_name=player_team_name, player_name=player_name)

            p.attributes['player_attack'] = int(player_row.find('.//td[8]/span').text)
            p.attributes['player_defending'] = int(player_row.find('.//td[9]/span').text)
            p.attributes['player_skill'] = int(player_row.find('.//td[10]/span').text)
            p.attributes['player_mentality'] = int(player_row.find('.//td[11]/span').text)
            p.attributes['player_power'] = int(player_row.find('.//td[12]/span').text)
            p.attributes['player_movement'] = int(player_row.find('.//td[13]/span').text)
            players_return_list.append(p)
            num_player_rows += 1

        if num_player_rows == 0:
            if len(players_return_list) == 0:  # TODO: logla bunu hiç oyuncu yoksa bir şeyler ters gitmiştir
                return None
            return players_return_list

        time.sleep(1)
        return self.get_player_data(base_url=base_url, page_index=page_index + 1,
                                    players_return_list=players_return_list, team_names_fix_dict=team_names_fix_dict)

    def scrape_players(self, league: League) -> Optional[List[Player]]:
        fm_version = league.value['players']['fm_version']
        league_id = league.value['players']['league_id']
        league_name = league.value['players']['league_name']

        base_url = f"https://fmdataba.com/{fm_version}/l/{league_id}/{league_name}/best-players/"
        return self.get_player_data(base_url=base_url,
                                    team_names_fix_dict=league.value['players']['team_names_fix_dict'])

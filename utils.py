import codecs
from os import path
from typing import List, Optional
import csv

from player import Player


def get_next_available_file_name(file_name: str, retry_num: int = 0) -> str:
    if retry_num == 0:
        if path.exists(file_name) is False:
            return file_name
        else:
            retry_num += 1
    else:
        if path.exists(file_name.split('.')[0] + f" ({str(retry_num)})." + file_name.split('.')[1]) is False:
            return file_name.split('.')[0] + f" ({str(retry_num)})." + file_name.split('.')[1]
    return get_next_available_file_name(file_name, retry_num + 1)


def write_players_to_csv(player_list: List[Player] = Player.all_players, file_name: str = "ftb2-player-data.csv"):
    file_name = get_next_available_file_name(file_name)
    with open(file_name, "w", encoding='utf-16') as csv_file:
        csv_file.write("player_id,player_name,player_team_id,player_team_name,player_attack,player_movement"
                       ",player_mentality,player_defending,player_power,player_skill\n")

        for player in Player.all_players.values():
            csv_file.write(player.as_csv_row() + "\n")


def read_players_from_csv(file_name: str = "ftb2-player-data.csv") -> Optional[List[Player]]:
    if path.exists(file_name) is False:
        return None
    player_return_list = []
    reader = csv.reader(codecs.open(file_name, 'rU', 'utf-16'), delimiter=',', quoting=csv.QUOTE_NONE)
    num_rows = 0
    for row in reader:
        if num_rows == 0:
            num_rows += 1
            continue
        else:
            player_return_list.append(Player.player_from_csv_row(csv_row=row))
    return player_return_list
